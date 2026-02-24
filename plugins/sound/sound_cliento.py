import os
import json
from PySide6.QtWidgets import QWidget, QButtonGroup
from PySide6.QtCore import Qt
from sound_save_load import load_sound_config, save_sound_config, update_selected_device

# Импорт UI
try:
    from resources.ui_done.ui_sound_cliento import Ui_sound_cliento
except ImportError:
    from .resources.ui_done.ui_sound_cliento import Ui_sound_cliento


class SoundClientoPlugin(QWidget, Ui_sound_cliento):
    """Виджет управления звуком с применением стилей."""

    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.plugin_path = plugin_path
        self.setupUi(self)
        
        # Инициализация логики
        try:
            from .sound_core import SoundCore
        except ImportError:
            from sound_core import SoundCore
        self.core = SoundCore(socket_client)
        
        self.load_stylesheet()
        self.setup_device_buttons()
        self.load_config_to_ui()
        self.bind_ui()

    def setup_device_buttons(self):
        """Настройка кнопок выбора устройства в группу."""
        self.device_group = QButtonGroup(self)
        self.device_group.setExclusive(True)
        
        buttons = [self.audiD_01_toolB, self.audiD_02_toolB]
        for i, btn in enumerate(buttons):
            btn.setCheckable(True)
            self.device_group.addButton(btn, i)
            
        self.device_group.idClicked.connect(self.save_selected_device)

    def save_selected_device(self, btn_id):
        """Сохраняет выбранное устройство в config_sound.json и отправляет на сервер."""
        config = load_sound_config(self.plugin_path)
        devices = config.get("output_devices", [])
        
        if 0 <= btn_id < len(devices):
            device_name = devices[btn_id]
            if update_selected_device(self.plugin_path, device_name):
                # Отправка на сервер через core
                if hasattr(self.core, 'socket_client') and self.core.socket_client:
                    self.core.socket_client.send_command(
                        "SOUND_SELECT_DEVICE",
                        {"device_name": device_name}
                    )

    def load_config_to_ui(self):
        """Отображает значения из config_sound.json в lineE элементах."""
        config = load_sound_config(self.plugin_path)
        if not config:
            return

        devices = config.get("output_devices", [])
        selected = config.get("selected_device", "")
        mute_state = config.get("mute_state", False)
        mic_mute_state = config.get("mic_mute_state", False)
        
        # Обновляем состояние кнопок Mute
        self.update_mute_ui("sound", mute_state)
        self.update_mute_ui("mic", mic_mute_state)

        # Обновляем слайдеры громкости
        self.sound_volume_slider.setValue(config.get("volume", 50))
        self.mic_volume_slider.setValue(config.get("mic_volume", 50))

        # Маппинг устройств на элементы формы
        ui_elements = [self.audiD_01_lineE, self.audiD_02_lineE]
        ui_buttons = [self.audiD_01_toolB, self.audiD_02_toolB]
        
        for i, device_name in enumerate(devices):
            if i < len(ui_elements):
                ui_elements[i].setText(device_name)
                ui_elements[i].setCursorPosition(0)
                # Активируем кнопку, если устройство выбрано
                if device_name == selected:
                    ui_buttons[i].setChecked(True)

    def bind_ui(self):
        """Привязка элементов UI к логике."""
        # Обработка команд от сервера
        if hasattr(self.core, 'socket_client') and self.core.socket_client:
            self.core.socket_client.message_received.connect(self.handle_server_message)

        # Слайдеры
        self.mic_volume_slider.sliderReleased.connect(lambda: self.on_volume_released("mic", self.mic_volume_slider.value()))
        self.sound_volume_slider.valueChanged.connect(lambda v: print(f"[SoundCliento] Volume changed: {v}"))
        self.sound_volume_slider.sliderReleased.connect(lambda: self.on_volume_released("sound", self.sound_volume_slider.value()))
        self.other_volume_slider.sliderReleased.connect(lambda: self.on_volume_released("other", self.other_volume_slider.value()))
        
        # Кнопки Mute
        self.mic_mute_toolB.clicked.connect(lambda: self.core.toggle_mute("mic"))
        self.sound_mute_toolB.clicked.connect(lambda: self.core.toggle_mute("sound"))
        self.other_mute_toolB.clicked.connect(lambda: self.core.toggle_mute("other"))
        
        # Обработка сигналов от core
        self.core.volume_changed.connect(self.update_volume_ui)
        self.core.mute_changed.connect(self.update_mute_ui)

    def on_volume_released(self, device, value):
        """Сохраняет громкость в конфиг и отправляет на сервер."""
        if getattr(self, "_block_broadcast", False):
            return

        # Сохранение через кэшируемую функцию
        key = "volume" if device == "sound" else f"{device}_volume"
        if save_sound_config(self.plugin_path, {key: value}):
            # Отправка на сервер через core
            self.core.set_volume(device, value)

    def update_volume_ui(self, device, value):
        if device == "mic":
            self.mic_volume_slider.setValue(value)
        elif device == "sound":
            self.sound_volume_slider.setValue(value)
        elif device == "other":
            self.other_volume_slider.setValue(value)

    def update_mute_ui(self, device, is_muted):
        style = "background-color: red;" if is_muted else ""
        if device == "mic":
            self.mic_mute_toolB.setStyleSheet(style)
        elif device == "sound":
            self.sound_mute_toolB.setStyleSheet(style)
        elif device == "other":
            self.other_mute_toolB.setStyleSheet(style)

    def handle_server_message(self, msg):
        """Обработка сообщений от сервера."""
        command = msg.get("command")
        data = msg.get("data", {})

        # Флаг для блокировки обратной отправки
        self._block_broadcast = True
        try:
            if command == "SOUND_UPDATE_DEVICES":
                if save_sound_config(self.plugin_path, data):
                    self.load_config_to_ui()
            
            elif command == "SOUND_TOGGLE_MUTE":
                payload = msg.get("payload", {})
                device, value = payload.get("device"), payload.get("value")
                if device and value is not None:
                    self.core.update_mute_state(device, value)
            
            elif command in ["SOUND_SET_MUTE", "SOUND_SET_VOLUME"]:
                device, value = data.get("device"), data.get("value")
                if device and value is not None:
                    if "VOLUME" in command: self.core.set_volume(device, value)
                    else: self.core.update_mute_state(device, value)
        finally:
            self._block_broadcast = False

    def load_stylesheet(self):
        """Загружает стиль из style_sound_cliento.json с привязкой к объекту."""
        style_path = os.path.join(self.plugin_path, "config", "style_sound_cliento.json")
        if not os.path.exists(style_path):
            return

        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                style_data = json.load(f)

            # Используем list comprehension для быстрой сборки
            css_blocks = []
            for selector, props in style_data.items():
                props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                # Если селектор не начинается с # или Q, можно добавить префикс для изоляции
                css_blocks.append(f"{selector} {{ {props_str} }}")

            final_css = "\n".join(css_blocks)
            
            # Устанавливаем стиль
            self.setStyleSheet(final_css)
            
            # Принудительное обновление стиля для корректного отображения
            self.style().unpolish(self)
            self.style().polish(self)
            
        except Exception as e:
            print(f"[SoundClientoPlugin] Error loading stylesheet: {e}")
