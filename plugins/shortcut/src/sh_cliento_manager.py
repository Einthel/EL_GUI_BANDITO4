import os
from PySide6.QtCore import QObject, Signal
try:
    from .sh_cliento_service import save_config, handle_icon_save
except ImportError:
    from sh_cliento_service import save_config, handle_icon_save

class ShortcutClientManager(QObject):
    """
    Координатор логики плагина. 
    Управляет состоянием, сетевыми командами и системными действиями.
    """
    config_updated = Signal(dict)
    page_change_requested = Signal(str) # "next", "prev"
    
    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.socket_client = socket_client
        self.plugin_path = plugin_path
        self.config = {}

    def set_config(self, config):
        self.config = config

    def on_server_message(self, data):
        """Диспетчер сообщений от сервера."""
        command = data.get("command")
        payload = data.get("data")
        
        if not payload:
            return

        if command == "SHORTCUT_CONFIG_UPDATE":
            self.handle_config_update(payload)
        elif command == "SHORTCUT_ICON_UPDATE":
            self.handle_icon_update(payload)

    def handle_icon_update(self, icon_data):
        """Сохранение иконки через сервис."""
        saved_path = handle_icon_save(self.plugin_path, icon_data)

    def handle_config_update(self, new_config):
        """Обновление конфига в памяти, на диске и уведомление UI."""
        self.config = new_config
        if save_config(self.plugin_path, new_config):
            self.config_updated.emit(new_config)

    def process_button_click(self, btn_id, page_id):
        """
        Решает, что делать при нажатии кнопки: 
        выполнить локальное действие или отправить на сервер.
        """
        page_num = page_id.replace("page_", "") if "page_" in page_id else "1"
        
        # Проверка локальных действий (system)
        if page_id in self.config and btn_id in self.config[page_id]:
            btn_props = self.config[page_id][btn_id]
            action = btn_props.get("action", {})
            
            if action.get("type") == "system":
                val = action.get("value")
                if val == "page_next":
                    self.page_change_requested.emit("next")
                    return
                elif val == "page_prev":
                    self.page_change_requested.emit("prev")
                    return

        # Если не системное — отправка на сервер
        self.send_to_server(f"{page_num}:{btn_id}")

    def get_button_props(self, btn_id, page_id):
        """Возвращает свойства кнопки из конфига."""
        if page_id in self.config and btn_id in self.config[page_id]:
            return self.config[page_id][btn_id]
        return None

    def send_to_server(self, payload_str):
        """Отправка команды на сервер через сокет."""
        if self.socket_client:
            self.socket_client.send_command("PLUGIN_BUTTON_PRESS", {"id": payload_str})

