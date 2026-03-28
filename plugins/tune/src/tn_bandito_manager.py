from PySide6.QtCore import QObject, Signal
import os
try:
    from .tn_cliento_service import TuneClientoService
except (ImportError, ValueError):
    from tn_cliento_service import TuneClientoService

class TuneClientoManager(QObject):
    """Уровень бизнес-логики для плагина Tune."""
    
    config_updated = Signal(dict)
    style_updated = Signal(str)

    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.socket_client = socket_client
        self.plugin_path = plugin_path
        self.service = TuneClientoService()
        self.config = {}
        self.config_path = os.path.join(self.plugin_path, "config", "config_tune.json")
        
        # Подписка на сообщения от сервера
        if self.socket_client:
            self.socket_client.message_received.connect(self.on_server_message)

    def load_initial_data(self):
        """Загрузка начальных данных при запуске."""
        style_path = os.path.join(self.plugin_path, "config", "style_tune_material.json")
        style_data = self.service.load_json_config(style_path)
        if style_data:
            css = self.service.json_to_css(style_data)
            self.style_updated.emit(css)

        # Первичная загрузка конфига плагина
        config_data = self.service.load_json_config(self.config_path)
        if isinstance(config_data, dict) and config_data:
            self.config = config_data
            self.config_updated.emit(config_data)

    def on_server_message(self, message):
        """Обработка входящих сообщений от сервера."""
        command = message.get("command")
        payload = message.get("data")

        if not payload:
            return

        if command == "TUNE_CONFIG_UPDATE":
            self._handle_config_update(payload)

    def _handle_config_update(self, new_config):
        """Обновление локального конфига и уведомление UI."""
        if not isinstance(new_config, dict):
            return

        self.config = new_config
        # Сохраняем актуальный конфиг на диск для клиента
        self.service.save_json_config(self.config_path, self.config)
        self.config_updated.emit(self.config)

    def send_button_press(self, button_id):
        """Отправка команды нажатия кнопки на сервер."""
        if self.socket_client:
            data = {
                "type": "PLUGIN_BUTTON_PRESS",
                "plugin_id": "tune",
                "button_id": button_id
            }
            self.socket_client.send_message(data)
