import os
import json
import importlib.util
from PySide6.QtWidgets import QWidget, QToolButton
try:
    from .src.tn_audio_manager import TnAudioManager
except (ImportError, SystemError, ValueError):
    # Фоллбек на прямой импорт, если пакетная структура отличается
    from src.tn_audio_manager import TnAudioManager

class TuneBanditoPlugin(QWidget):
    """Серверная логика плагина Tune."""

    def __init__(self, plugin_path, core=None):
        super().__init__()
        self.plugin_path = plugin_path
        self.core = core
        self.config_path = os.path.join(self.plugin_path, "config", "config_tune.json")
        self.audio_manager = TnAudioManager()
        
        # Изолированный импорт UI
        self.ui = self._load_ui()
        self.ui.setupUi(self)
        
        self._load_config()
        self._apply_styles()
        self._connect_signals()
        self._log_output_devices_on_start()
        # Отправляем актуальный конфиг клиентам при загрузке плагина
        self.broadcast_update()

    def _apply_styles(self):
        """Загрузка и применение стилей из JSON."""
        style_path = os.path.join(self.plugin_path, "config", "style_tune_material.json")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)
                css = ""
                for selector, props in style_data.items():
                    props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                    css += f"{selector} {{ {props_str} }} \n"
                self.setStyleSheet(css)
            except Exception as e:
                print(f"[Tn] Style: {e}")

    def _log_output_devices_on_start(self):
        """Запрос и логирование доступных аудиоустройств при загрузке плагина."""
        try:
            # 1. Выходные устройства
            out_devices = self.audio_manager.refresh_output_devices()
            if out_devices:
                if not isinstance(getattr(self, "config", None), dict):
                    self.config = {}
                # Не перезаписываем config["output_devices"] автоматически при старте,
                # чтобы сохранить "жесткий список", заданный пользователем.
                
                self._populate_output_device_combos(out_devices)
                self._populate_bluetooth_combo(out_devices)
                
                # Синхронизация мута звука при старте
                selected_name = self.config.get("selected_device")
                if not selected_name and out_devices:
                    selected_name = out_devices[0]
                
                if selected_name:
                    saved_mute = self.config.get("output_devices_muted", False)
                    saved_volume = self.config.get("output_devices_volume", 50)
                    self.audio_manager.set_mute_sound(selected_name, saved_mute)
                    self.audio_manager.set_device_volume(selected_name, saved_volume)
                    
                    btn = getattr(self.ui, "test_mute_sound_toolB", None)
                    if btn:
                        btn.setText("Muted" if saved_mute else "Sound")
                    
                    # Запускаем прослушивание статуса звука
                    self.audio_manager.start_sound_listening(selected_name, self._on_sound_status_changed_external)
            else:
                print("[Tn] No output devices")

            # 2. Входные устройства (микрофоны)
            in_devices = self.audio_manager.refresh_input_devices()
            if in_devices:
                # Сохраняем список всех микрофонов для выбора, но не затираем текущий selected_mic
                self.config["input_devices"] = in_devices
                self._populate_mic_combo(in_devices)
            
            self._write_config_to_disk()
        except Exception as e:
            print(f"[Tn] Audio devices init: {e}")

    def _populate_output_device_combos(self, devices: list[str]):
        """Заполнить основные комбобоксы списка аудиовыходов."""
        combo_names = ["audiD_01_comboB", "audiD_02_comboB"]
        saved_devices = self.config.get("output_devices", [])
        
        for idx, name in enumerate(combo_names):
            combo = getattr(self.ui, name, None)
            if combo is None: continue
            
            combo.blockSignals(True)
            combo.clear()
            
            # Добавляем все активные устройства
            combo.addItems(devices)
            
            # Если сохраненное устройство сейчас не в списке активных, 
            # добавляем его, чтобы сохранить "жесткий список" в UI
            if idx < len(saved_devices):
                saved_name = saved_devices[idx]
                if saved_name and saved_name not in devices:
                    combo.addItem(saved_name)
                combo.setCurrentText(saved_name)
            
            combo.blockSignals(False)

    def _populate_bluetooth_combo(self, devices: list[str]):
        """Отфильтровать и заполнить Bluetooth-устройства."""
        combo = getattr(self.ui, "bt_audiD_comboB", None)
        if combo is None: return

        bt_keywords = ["bluetooth", "airpods", "hands-free", "stereo", "bt "]
        bt_devices = [d for d in devices if any(k in d.lower() for k in bt_keywords)]
        
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(bt_devices)
        
        saved_bt = self.config.get("selected_bt_device")
        if saved_bt and saved_bt in bt_devices:
            combo.setCurrentText(saved_bt)
        elif bt_devices:
            combo.setCurrentIndex(0)
        combo.blockSignals(False)

    def _populate_mic_combo(self, devices: list[str]):
        """Заполнить список микрофонов."""
        combo = getattr(self.ui, "mic_01_comboB", None)
        if combo is None: return

        combo.blockSignals(True)
        combo.clear()
        combo.addItems(devices)
        
        saved_mic = self.config.get("selected_mic")
        if saved_mic and saved_mic in devices:
            combo.setCurrentText(saved_mic)
        elif devices:
            combo.setCurrentIndex(0)
        combo.blockSignals(False)

        # Синхронизация текста кнопки мута при загрузке
        mic_name = combo.currentText()
        if mic_name:
            # Применяем сохраненное состояние мута при старте
            saved_mute = self.config.get("input_devices_muted", False)
            saved_volume = self.config.get("input_devices_volume", 50)
            self.audio_manager.set_mute_mic(mic_name, saved_mute)
            self.audio_manager.set_device_volume(mic_name, saved_volume)
            
            btn = getattr(self.ui, "test_mute_toolB", None)
            if btn:
                btn.setText("Muted" if saved_mute else "Mute")

            # Запускаем прослушивание статуса
            self.audio_manager.start_mic_listening(mic_name, self._on_mic_status_changed_external)

    def _on_mic_status_changed_external(self, data: dict):
        """Обработка внешнего изменения статуса микрофона (системного)."""
        is_muted = data.get('mute')
        volume = data.get('volume')
        
        changed = False
        if is_muted is not None and self.config.get("input_devices_muted") != is_muted:
            self.config["input_devices_muted"] = is_muted
            changed = True
            
        if volume is not None and self.config.get("input_devices_volume") != volume:
            self.config["input_devices_volume"] = volume
            changed = True

        if not changed:
            return

        self._write_config_to_disk()

        btn = getattr(self.ui, "test_mute_toolB", None)
        if btn and is_muted is not None:
            btn.setText("Muted" if is_muted else "Mute")
        
        self.broadcast_update()

    def _on_sound_status_changed_external(self, data: dict):
        """Обработка внешнего изменения статуса звука (системного)."""
        is_muted = data.get('mute')
        volume = data.get('volume')
        
        changed = False
        if is_muted is not None and self.config.get("output_devices_muted") != is_muted:
            self.config["output_devices_muted"] = is_muted
            changed = True
            
        if volume is not None and self.config.get("output_devices_volume") != volume:
            self.config["output_devices_volume"] = volume
            changed = True

        if not changed:
            return

        self._write_config_to_disk()

        btn = getattr(self.ui, "test_mute_sound_toolB", None)
        if btn and is_muted is not None:
            btn.setText("Muted" if is_muted else "Sound")
        
        self.broadcast_update()

    def _load_ui(self):
        """Динамический импорт UI для изоляции ресурсов."""
        ui_path = os.path.join(self.plugin_path, "resources", "ui_done", "ui_tune_bandito.py")
        spec = importlib.util.spec_from_file_location("ui_tune_bandito", ui_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Ui_tune_bandito()

    def _load_config(self):
        """Загрузка конфигурации плагина."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def _write_config_to_disk(self):
        """Служебный метод: сохранить конфиг на диск без broadcast."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def _connect_signals(self):
        """Подключение сигналов интерфейса."""
        # Кнопка сохранения
        button = getattr(self.ui, "output_device_save_toolB", None)
        if button is None:
            button = self.findChild(QToolButton, "output_device_save_toolB")
        if button is not None:
            button.clicked.connect(self.save_config)

        # Взаимоисключающий выбор для основных выходов
        combos = ["audiD_01_comboB", "audiD_02_comboB"]
        for i, name in enumerate(combos, start=1):
            combo = getattr(self.ui, name, None)
            if combo:
                combo.currentIndexChanged.connect(lambda idx, s=i: self._on_output_combo_changed(s, idx))

        # Кнопка мута микрофона
        mute_btn = getattr(self.ui, "test_mute_toolB", None)
        if mute_btn:
            mute_btn.clicked.connect(self._toggle_mic_mute)

        # Кнопка мута звука
        sound_mute_btn = getattr(self.ui, "test_mute_sound_toolB", None)
        if sound_mute_btn:
            sound_mute_btn.clicked.connect(self._toggle_sound_mute)

        # Выбор микрофона
        mic_combo = getattr(self.ui, "mic_01_comboB", None)
        if mic_combo:
            mic_combo.currentIndexChanged.connect(self._on_mic_combo_changed)

    def _on_mic_combo_changed(self, index: int):
        """Смена активного микрофона для прослушивания."""
        combo = getattr(self.ui, "mic_01_comboB", None)
        if not combo: return
        
        mic_name = combo.currentText()
        if not mic_name: return

        # Обновляем текущее состояние мута и громкости для нового устройства
        is_muted = self.audio_manager.is_mic_muted(mic_name)
        volume = self.audio_manager.get_device_volume(mic_name)
        self.config["selected_mic"] = mic_name
        self.config["input_devices_muted"] = is_muted
        self.config["input_devices_volume"] = volume
        
        # Обновляем UI
        btn = getattr(self.ui, "test_mute_toolB", None)
        if btn:
            btn.setText("Muted" if is_muted else "Mute")

        # Перезапуск слушателя
        self.audio_manager.start_mic_listening(mic_name, self._on_mic_status_changed_external)
        
        # Сохраняем и уведомляем
        self._write_config_to_disk()
        self.broadcast_update()

    def _toggle_mic_mute(self):
        """Переключить состояние мута выбранного микрофона."""
        mic_name = self.config.get("selected_mic")
        if not mic_name:
            combo = getattr(self.ui, "mic_01_comboB", None)
            mic_name = combo.currentText() if combo else None
        
        if not mic_name:
            return

        is_muted = self.audio_manager.is_mic_muted(mic_name)
        new_state = not is_muted
        if self.audio_manager.set_mute_mic(mic_name, new_state):
            # Сохраняем состояние в конфиг
            self.config["input_devices_muted"] = new_state
            self._write_config_to_disk()
            
            # Визуальное уведомление на кнопке сервера
            btn = getattr(self.ui, "test_mute_toolB", None)
            if btn:
                btn.setText("Muted" if new_state else "Mute")
            
            # Рассылаем обновление всем клиентам
            self.broadcast_update()

    def _on_output_combo_changed(self, slot_index: int, index: int):
        """Гарантировать, что в двух основных комбобоксах не выбрано одно и то же устройство."""
        devices = self.audio_manager.get_cached_output_devices()
        if not devices or index < 0 or index >= len(devices):
            return

        selected_name = devices[index]
        other_idx = 1 if slot_index == 2 else 2
        other_combo = getattr(self.ui, f"audiD_0{other_idx}_comboB", None)

        if other_combo and other_combo.currentText() == selected_name:
            # Смещаем другой комбобокс на следующее доступное устройство
            for i, name in enumerate(devices):
                if name != selected_name:
                    other_combo.blockSignals(True)
                    other_combo.setCurrentIndex(i)
                    other_combo.blockSignals(False)
                    break

    def save_config(self):
        """Сохранение конфигурации и уведомление клиентов."""
        self._apply_all_selections_to_config()
        self._write_config_to_disk()
        self._apply_selected_device_to_system()
        self.broadcast_update()

    def _apply_all_selections_to_config(self):
        """Считать выбор из ВСЕХ комбобоксов и зафиксировать его в конфиге."""
        if not isinstance(getattr(self, "config", None), dict):
            self.config = {}

        # 1. Основные выходы (жесткий список из двух элементов)
        c1 = getattr(self.ui, "audiD_01_comboB", None)
        c2 = getattr(self.ui, "audiD_02_comboB", None)
        
        sel1 = c1.currentText().strip() if c1 else ""
        sel2 = c2.currentText().strip() if c2 else ""
        
        # Сохраняем именно эти два устройства как основной список для RPi
        self.config["output_devices"] = [sel1, sel2]

        # 2. Bluetooth устройство
        bt_combo = getattr(self.ui, "bt_audiD_comboB", None)
        if bt_combo:
            self.config["selected_bt_device"] = bt_combo.currentText()

        # 3. Микрофон
        mic_combo = getattr(self.ui, "mic_01_comboB", None)
        if mic_combo:
            self.config["selected_mic"] = mic_combo.currentText()

    def _apply_selected_device_to_system(self):
        """Применить выбранное в конфиге устройство как системное по умолчанию."""
        if not isinstance(getattr(self, "config", None), dict):
            return

        selected = self.config.get("selected_device") or ""
        if not selected:
            print("[Tn] No selected_device")
            return

        ok = self.audio_manager.set_default_output_device(selected)
        if ok:
            # Обновляем состояние мута и громкости для нового устройства в UI
            is_muted = self.audio_manager.is_sound_muted(selected)
            volume = self.audio_manager.get_device_volume(selected)
            self.config["output_devices_muted"] = is_muted
            self.config["output_devices_volume"] = volume
            
            btn = getattr(self.ui, "test_mute_sound_toolB", None)
            if btn:
                btn.setText("Muted" if is_muted else "Sound")
            
            # Перезапускаем прослушивание статуса для нового устройства
            self.audio_manager.start_sound_listening(selected, self._on_sound_status_changed_external)
        else:
            print(f"[Tn] Failed: {selected}")

    def handle_button_press(self, btn_id, payload=None):
        """Обязательный метод для обработки событий от клиента (PLUGIN_BUTTON_PRESS)."""
        # Нормализация btn_id и payload
        if isinstance(btn_id, dict):
            payload = btn_id
            btn_id = payload.get("id")
        
        if payload and not btn_id:
            btn_id = payload.get("id")
            
        # Парсинг упакованного значения из ID (формат "id|value")
        extracted_value = None
        if isinstance(btn_id, str) and "|" in btn_id:
            try:
                parts = btn_id.split("|")
                btn_id = parts[0]
                extracted_value = int(parts[1])
            except (ValueError, IndexError):
                pass
        
        # Обработка изменения громкости со слайдеров
        if btn_id in ["sound_volume_slider", "mic_volume_slider"]:
            val = extracted_value
            if val is None and isinstance(payload, dict):
                val = payload.get("value") or payload.get("val") or payload.get("data")
            
            dev_type = "sound" if btn_id == "sound_volume_slider" else "mic"
            self._set_volume_from_client(dev_type, val)
            return

        # Специальная обработка кнопок выбора устройства на клиенте
        if btn_id == "audiD_01_toolB":
            self._select_device_by_index(0)
        elif btn_id == "audiD_02_toolB":
            self._select_device_by_index(1)
        elif btn_id == "bt_audiD_toolB":
            self._select_bt_device()
        elif btn_id in ["mic_mute_toolB", "test_mute_toolB"]:
            self._toggle_mic_mute()
        elif btn_id in ["sound_mute_toolB", "test_mute_sound_toolB"]:
            self._toggle_sound_mute()

    def _set_volume_from_client(self, dev_type: str, value: int):
        """Применить новое значение громкости с клиента."""
        if value is None: 
            return
        
        # Конфигурация для разных типов устройств
        cfg = {
            "sound": {
                "key": "selected_device",
                "vol_key": "output_devices_volume",
                "get_devs": self.audio_manager.get_cached_output_devices
            },
            "mic": {
                "key": "selected_mic",
                "vol_key": "input_devices_volume",
                "get_devs": self.audio_manager.get_cached_input_devices
            }
        }.get(dev_type)

        if not cfg:
            return

        device_name = self.config.get(cfg["key"])
        if not device_name:
            devices = cfg["get_devs"]()
            device_name = devices[0] if devices else None
        
        if device_name and self.audio_manager.set_device_volume(device_name, value):
            self.config[cfg["vol_key"]] = value
            self._write_config_to_disk()
            self.broadcast_update()

    def _toggle_sound_mute(self):
        """Переключить состояние мута выбранного устройства вывода."""
        device_name = self.config.get("selected_device")
        if not device_name:
            out_devices = self.audio_manager.get_cached_output_devices()
            device_name = out_devices[0] if out_devices else None
        
        if not device_name:
            return

        is_muted = self.audio_manager.is_sound_muted(device_name)
        new_state = not is_muted
        if self.audio_manager.set_mute_sound(device_name, new_state):
            self.config["output_devices_muted"] = new_state
            self._write_config_to_disk()
            
            btn = getattr(self.ui, "test_mute_sound_toolB", None)
            if btn:
                btn.setText("Muted" if new_state else "Sound")
            
            self.broadcast_update()

    def _select_bt_device(self):
        """Выбрать сохраненное BT устройство, применить и разослать."""
        if not isinstance(getattr(self, "config", None), dict):
            return
            
        selected = self.config.get("selected_bt_device")
        if not selected:
            print("[Tn] No BT device selected in config")
            return
            
        # Проверка доступности устройства перед переключением
        active_devices = self.audio_manager.refresh_output_devices()
        if selected not in active_devices:
            print(f"[Tn] BT Device '{selected}' is offline. Switching cancelled.")
            return

        self.config["selected_device"] = selected
        self._write_config_to_disk()
        self._apply_selected_device_to_system()
        self.broadcast_update()

    def _select_device_by_index(self, index: int):
        """Выбрать устройство по индексу в config['output_devices'], применить и разослать."""
        if not isinstance(getattr(self, "config", None), dict):
            self.config = {}

        devices = self.config.get("output_devices") or []
        if not devices or index < 0 or index >= len(devices):
            print(f"[Tn] No device @{index}")
            return

        selected = devices[index]
        
        # Проверка доступности устройства перед переключением
        active_devices = self.audio_manager.refresh_output_devices()
        if selected not in active_devices:
            print(f"[Tn] Device '{selected}' is offline. Switching cancelled.")
            return

        self.config["selected_device"] = selected
        self._write_config_to_disk()
        self._apply_selected_device_to_system()
        self.broadcast_update()

    def broadcast_update(self):
        """Рассылка обновлений всем подключенным клиентам через Core."""
        if not self.core or not self.core.com:
            return
        try:
            # Добавляем список реально активных устройств в payload для клиента
            payload = self.config.copy()
            payload["active_devices"] = self.audio_manager.refresh_output_devices()
            self.core.com.broadcast("TUNE_CONFIG_UPDATE", payload)
        except Exception as e:
            print(f"[Tn] Broadcast: {e}")
