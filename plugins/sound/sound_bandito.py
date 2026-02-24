import os
import sys
import json
try:
    from loguru import logger
except ImportError:
    class DummyLogger:
        def debug(self, msg): print(f"DEBUG: {msg}")
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def success(self, msg): print(f"SUCCESS: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
    logger = DummyLogger()

# Глобальный список для предотвращения GC-крашей
_GLOBAL_AUDIO_KEEP_ALIVE = []

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from sound_save_load import load_sound_config, save_sound_config

# Добавляем корень проекта в sys.path для доступа к libs
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Импорт UI
try:
    from resources.ui_done.ui_sound_bandito import Ui_sound_bandito
except ImportError:
    from .resources.ui_done.ui_sound_bandito import Ui_sound_bandito


class SoundBanditoPlugin(QWidget, Ui_sound_bandito):
    """Виджет управления звуком Bandito."""

    def __init__(self, socket_client=None, plugin_path=None):
        super().__init__()
        self.socket_client = socket_client
        self.plugin_path = plugin_path if plugin_path else os.path.dirname(__file__)
        self.setupUi(self)
        
        # Инициализация логики
        try:
            from .sound_core import SoundCore
        except ImportError:
            from sound_core import SoundCore
        self.core = SoundCore(socket_client=self.socket_client)
        
        # Таймер для отложенного сохранения громкости (debounce)
        from PySide6.QtCore import QTimer
        self.volume_save_timer = QTimer()
        self.volume_save_timer.setSingleShot(True)
        self.volume_save_timer.setInterval(500)
        self.volume_save_timer.timeout.connect(self.commit_volume_changes)
        self._pending_volume_updates = {}
        
        self.setup_server_callbacks()
        self.load_stylesheet()
        self.update_device_lists()
        self.check_initial_mute_state()
        self.apply_config_volume()
        self.load_config()

        # Подключение сигналов
        self.outpu_device_save_toolB.clicked.connect(self.save_config)
        
        # Отслеживание изменений из core (системные события)
        self.core.mute_changed.connect(self.on_core_mute_changed)
        self.core.volume_changed.connect(self.on_core_volume_changed)
        
        # Подключение обработки сообщений от клиента
        if hasattr(self.socket_client, 'message_received'):
            self.socket_client.message_received.connect(self.handle_client_message)

    def apply_config_volume(self):
        """Применяет громкость из конфига к системе при запуске."""
        config = load_sound_config(self.plugin_path)
        if not config:
            return
            
        # Применяем общую громкость
        volume = config.get("volume")
        if volume is not None:
            self.core.set_volume("sound", volume)
            
        # Применяем громкость микрофона
        mic_volume = config.get("mic_volume")
        if mic_volume is not None:
            self.core.set_volume("mic", mic_volume)

    def setup_server_callbacks(self):
        """Регистрация колбэков только на стороне сервера."""
        try:
            import pythoncom
            pythoncom.CoInitialize()
            
            import comtypes
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioEndpointVolumeCallback
            from ctypes import POINTER, cast
            from comtypes import CLSCTX_ALL
            from PySide6.QtCore import QObject, Signal

            # Вспомогательный класс для безопасной передачи данных между потоками
            class AudioSignalEmitter(QObject):
                notify = Signal(str, bool, int) # device_type, is_muted, volume

            if not hasattr(self, 'audio_emitter'):
                self.audio_emitter = AudioSignalEmitter()
                self.audio_emitter.notify.connect(self._handle_notify_signal)

            class AudioCallback(comtypes.COMObject):
                _com_interfaces_ = [IAudioEndpointVolumeCallback]
                def __init__(self, emitter, device_type):
                    super().__init__()
                    self.emitter = emitter
                    self.device_type = device_type
                
                def OnNotify(self, pNotify):
                    try:
                        is_muted = bool(pNotify.contents.bMuted)
                        volume = int(pNotify.contents.fMasterVolume * 100)
                        logger.debug(f"[AudioCallback] System notify: {self.device_type} | Mute: {is_muted} | Vol: {volume}")
                        # Эмитим сигнал, который придет в основной поток Qt
                        self.emitter.notify.emit(self.device_type, is_muted, volume)
                    except Exception as e:
                        logger.error(f"[AudioCallback] Error in OnNotify: {e}")
                    return 0

            self._audio_callbacks_refs = [] # Жесткие ссылки для GC
            for dev_type in ["sound", "mic"]:
                logger.info(f"[SoundBandito] Registering callback for {dev_type}")
                
                # Сохраняем ссылки на ВСЕ промежуточные объекты
                device = AudioUtilities.GetMicrophone() if dev_type == "mic" else AudioUtilities.GetSpeakers()
                interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                
                callback = AudioCallback(self.audio_emitter, dev_type)
                volume_interface.RegisterControlChangeNotify(callback)
                
                # Добавляем в ГЛОБАЛЬНЫЙ список, который НИКОГДА не очищается GC
                global _GLOBAL_AUDIO_KEEP_ALIVE
                _GLOBAL_AUDIO_KEEP_ALIVE.append((device, interface, volume_interface, callback))
                
                self._audio_callbacks_refs.append((device, interface, volume_interface, callback))
                self.core._callbacks[dev_type] = (volume_interface, callback)
                
            logger.success("[SoundBandito] Системные колбэки успешно зарегистрированы")
        except Exception as e:
            logger.error(f"[SoundBandito] Ошибка регистрации системных колбэков: {e}")

    def _handle_notify_signal(self, device_type, is_muted, volume):
        """Обработка сигнала из COM-потока в основном потоке Qt."""
        self.core.handle_system_mute_change(device_type, is_muted)
        self.core.handle_system_volume_change(device_type, volume)

    def on_core_mute_changed(self, device, is_muted):
        """Вызывается при изменении Mute в системе."""
        config = load_sound_config(self.plugin_path)
        key = "mute_state" if device == "sound" else "mic_mute_state"
        if config.get(key) != is_muted:
            if save_sound_config(self.plugin_path, {key: is_muted}):
                self.broadcast_config(load_sound_config(self.plugin_path))

    def on_core_volume_changed(self, device, volume):
        """Вызывается при изменении громкости в системе. Использует debounce."""
        self._pending_volume_updates[device] = volume
        self.volume_save_timer.start()

    def commit_volume_changes(self):
        """Окончательное сохранение накопленных изменений громкости."""
        if not self._pending_volume_updates:
            return
            
        updates = {}
        for device, volume in self._pending_volume_updates.items():
            key = "volume" if device == "sound" else "mic_volume"
            updates[key] = volume
        
        if save_sound_config(self.plugin_path, updates):
            self.broadcast_config(load_sound_config(self.plugin_path))
                
        self._pending_volume_updates.clear()

    def check_initial_mute_state(self):
        """Проверяет начальное состояние звука и обновляет конфиг."""
        updates = {
            "mute_state": self.core.get_mute_state("sound"),
            "mic_mute_state": self.core.get_mute_state("mic"),
            "volume": self.core.get_system_volume("sound"),
            "mic_volume": self.core.get_system_volume("mic")
        }
        
        if save_sound_config(self.plugin_path, updates):
            self.broadcast_config(load_sound_config(self.plugin_path))

    def handle_client_message(self, msg):
        """Обработка команд от клиента."""
        if not msg or not isinstance(msg, dict): return
        command = msg.get("command")
        payload = msg.get("payload") or msg.get("data") or {}

        # Флаг для блокировки обратной отправки
        self._block_broadcast = True
        try:
            if command == "SOUND_SELECT_DEVICE":
                device_name = payload.get("device_name")
                if device_name: self.core.set_device(device_name)

            elif command == "SOUND_TOGGLE_MUTE":
                device, value = payload.get("device"), payload.get("value")
                if device and value is not None:
                    self.core.set_mute(device, value)
                    self.on_core_mute_changed(device, value)

            elif command == "SOUND_SET_VOLUME":
                device, value = payload.get("device"), payload.get("value")
                if device and value is not None:
                    # Установка громкости в системе
                    self.core.set_volume(device, value)
                    # Сохранение в конфиг
                    self.on_core_volume_changed(device, value)
        finally:
            self._block_broadcast = False

    def update_device_lists(self):
        """Обновляет списки аудиоустройств в комбобоксах."""
        devices = self.core.get_all_devices()
        combos = [self.audiD_01_comboB, self.audiD_02_comboB]
        
        for combo in combos:
            combo.clear()
            combo.addItem("")
            combo.addItems(devices)

        mics = self.core.get_all_mic()
        self.mic_01_comboB.clear()
        self.mic_01_comboB.addItem("")
        self.mic_01_comboB.addItems(mics)

    def load_config(self):
        """Загружает сохраненные устройства из конфига."""
        config = load_sound_config(self.plugin_path)
        if not config:
            return

        devices = config.get("output_devices", [])
        combos = [self.audiD_01_comboB, self.audiD_02_comboB]
        
        for i, device_name in enumerate(devices):
            if i < len(combos):
                index = combos[i].findText(device_name)
                if index >= 0:
                    combos[i].setCurrentIndex(index)

        mic_name = config.get("mic_device", "")
        if mic_name:
            index = self.mic_01_comboB.findText(mic_name)
            if index >= 0:
                self.mic_01_comboB.setCurrentIndex(index)

    def save_config(self):
        """Сохраняет выбранные устройства в конфиг."""
        combos = [self.audiD_01_comboB, self.audiD_02_comboB]
        
        config_data = load_sound_config(self.plugin_path) or {}
        config_data.update({
            "output_devices": [combo.currentText() for combo in combos],
            "mic_device": self.mic_01_comboB.currentText()
        })
        
        if save_sound_config(self.plugin_path, config_data):
            self.broadcast_config(config_data)

    def broadcast_config(self, config_data):
        """Передача обновленного конфига на клиент."""
        if getattr(self, "_block_broadcast", False):
            return

        if self.socket_client:
            payload = {
                "command": "SOUND_UPDATE_DEVICES",
                "data": config_data
            }
            try:
                # Определение корня проекта для поиска конфига сервера
                p_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                server_config_path = os.path.join(p_root, "configs", "el_bandito_config.json")
                port = 8000
                if os.path.exists(server_config_path):
                    with open(server_config_path, 'r') as f:
                        port = json.load(f).get("port", 8000)
                        
                url = f"http://127.0.0.1:{port}/api/broadcast"
                
                # Используем urllib вместо requests для стабильности в потоках
                import urllib.request
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=0.5) as response:
                    pass
            except Exception as e:
                logger.warning(f"[SoundBandito] Broadcast failed: {e}")

    def __del__(self):
        """Очистка при удалении виджета."""
        try:
            import pythoncom
            pythoncom.CoInitialize()
            for volume_interface, callback in self._audio_callbacks_refs:
                try:
                    logger.info(f"[SoundBandito] Unregistering callback")
                    volume_interface.UnregisterControlChangeNotify(callback)
                except Exception as e:
                    logger.error(f"[SoundBandito] Unregister error: {e}")
            pythoncom.CoUninitialize()
        except Exception as e:
            pass

    def load_stylesheet(self):
        """Загружает стиль из style_sound_bandito.json."""
        style_path = os.path.join(self.plugin_path, "config", "style_sound_bandito.json")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)

                css = ""
                for selector, props in style_data.items():
                    props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                    css += f"{selector} {{ {props_str} }} \n"

                self.setStyleSheet(css)
            except:
                pass
