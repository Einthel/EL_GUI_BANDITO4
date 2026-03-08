import os
from PySide6.QtCore import QObject, Signal
try:
    from .sh_bandito_service import (
        load_json, save_json,
        prepare_icon_payload, execute_system_action
    )
except ImportError:
    from sh_bandito_service import (
        load_json, save_json,
        prepare_icon_payload, execute_system_action
    )

class ShortcutBanditoManager(QObject):
    """
    Менеджер логики для серверной части (редактора).
    Управляет конфигами, префабами и синхронизацией с клиентами.
    """
    config_updated = Signal()
    page_changed = Signal(int)
    
    def __init__(self, plugin_path, core=None):
        super().__init__()
        self.plugin_path = plugin_path
        self.core = core
        
        # Пути к файлам
        self.config_path = os.path.join(self.plugin_path, "config", "button_shortcut.json")
        self.prefab_path = os.path.join(self.plugin_path, "config", "prefab_but_shortcut.json")
        self.actions_path = os.path.join(self.plugin_path, "config", "config_shortcut.json")
        
        # Данные
        self.config_data = load_json(self.config_path)
        self.prefabs = load_json(self.prefab_path)
        self.actions_config = load_json(self.actions_path)
        
        # Состояние
        self.current_page = 1

    def get_data(self):
        return self.config_data

    def get_prefabs(self):
        """Возвращает словарь префабов. Если в JSON есть корневой ключ 'prefabs', возвращает его содержимое."""
        if isinstance(self.prefabs, dict) and "prefabs" in self.prefabs:
            return self.prefabs["prefabs"]
        return self.prefabs

    def get_actions(self):
        return self.actions_config.get("actions", [])

    def save_all(self):
        """Сохранение всех данных на диск."""
        save_json(self.config_path, self.config_data)
        save_json(self.prefab_path, self.prefabs)

    def update_button(self, page_idx, btn_name, btn_data):
        """Обновление данных кнопки на странице."""
        page_key = f"page_{page_idx}"
        if page_key not in self.config_data:
            self.config_data[page_key] = {}
        
        self.config_data[page_key][btn_name] = btn_data
        self.save_all()
        self.sync_with_clients(icon_rel_path=btn_data.get("icon_path"))
        self.config_updated.emit()

    def delete_button(self, page_idx, btn_name):
        """Удаление кнопки со страницы."""
        page_key = f"page_{page_idx}"
        if page_key in self.config_data and btn_name in self.config_data[page_key]:
            del self.config_data[page_key][btn_name]
            self.save_all()
            self.sync_with_clients()
            self.config_updated.emit()

    def add_new_page(self):
        """Добавление новой страницы."""
        indices = [int(k.split('_')[1]) for k in self.config_data.keys() if k.startswith("page_")]
        new_idx = max(indices) + 1 if indices else 1
        self.config_data[f"page_{new_idx}"] = {}
        self.save_all()
        self.sync_with_clients()
        return new_idx

    def remove_page(self, page_idx):
        """Удаление страницы и переиндексация оставшихся."""
        page_key = f"page_{page_idx}"
        if page_key in self.config_data:
            del self.config_data[page_key]
            
            # Переиндексация страниц для исключения дырок (1, 3 -> 1, 2)
            new_config = {}
            # Получаем все ключи страниц и сортируем их по номеру
            page_keys = [k for k in self.config_data.keys() if k.startswith("page_")]
            sorted_keys = sorted(page_keys, key=lambda x: int(x.split('_')[1]))
            
            for i, old_key in enumerate(sorted_keys, 1):
                new_config[f"page_{i}"] = self.config_data[old_key]
            
            # Сохраняем остальные ключи (не страницы), если они есть
            for k, v in self.config_data.items():
                if not k.startswith("page_"):
                    new_config[k] = v
            
            self.config_data = new_config
            self.save_all()
            self.sync_with_clients()
            self.config_updated.emit() # УВЕДОМЛЯЕМ UI ОБ ИЗМЕНЕНИИ СТРУКТУРЫ
        
        # Возвращаем ближайший существующий индекс
        indices = [int(k.split('_')[1]) for k in self.config_data.keys() if k.startswith("page_")]
        if not indices: return 1
        
        # Если текущий индекс больше максимального после удаления
        if page_idx > max(indices):
            return max(indices)
        return page_idx

    def save_prefab(self, name, data):
        """Сохранение префаба."""
        prefabs_dict = self.get_prefabs()
        prefabs_dict[name] = data
        
        # Если структура с корневым ключом, сохраняем её
        if isinstance(self.prefabs, dict) and "prefabs" in self.prefabs:
             self.prefabs["prefabs"] = prefabs_dict
        else:
             self.prefabs = prefabs_dict
             
        self.save_all()

    def delete_prefab(self, name):
        """Удаление префаба."""
        prefabs_dict = self.get_prefabs()
        if name in prefabs_dict:
            del prefabs_dict[name]
            
            if isinstance(self.prefabs, dict) and "prefabs" in self.prefabs:
                self.prefabs["prefabs"] = prefabs_dict
            else:
                self.prefabs = prefabs_dict
                
            self.save_all()

    def rename_prefab(self, old_name, new_name):
        """Переименование префаба."""
        prefabs_dict = self.get_prefabs()
        if old_name in prefabs_dict:
            prefabs_dict[new_name] = prefabs_dict.pop(old_name)
            
            if isinstance(self.prefabs, dict) and "prefabs" in self.prefabs:
                self.prefabs["prefabs"] = prefabs_dict
            else:
                self.prefabs = prefabs_dict
                
            self.save_all()

    def sync_with_clients(self, icon_rel_path=None):
        """Синхронизация конфига и иконок с клиентами через Core."""
        if not self.core or not self.core.com:
            print("[ShortcutManager] No core/com available for broadcast")
            return
        try:
            if icon_rel_path:
                icon_payload = prepare_icon_payload(self.plugin_path, icon_rel_path)
                if icon_payload:
                    self.core.com.broadcast("SHORTCUT_ICON_UPDATE", icon_payload)
            self.core.com.broadcast("SHORTCUT_CONFIG_UPDATE", self.config_data)
        except Exception as e:
            print(f"[ShortcutManager] Broadcast error: {e}")

    def handle_remote_press(self, btn_id_full):
        """Обработка нажатия кнопки (приходит от ElCore сервера)."""
        try:
            if ":" in btn_id_full:
                page_num, btn_name = btn_id_full.split(":")
                page_key = f"page_{page_num}"
            else:
                page_key = "page_1"
                btn_name = btn_id_full

            btn_data = self.config_data.get(page_key, {}).get(btn_name, {})
            action = btn_data.get("action")
            if action:
                execute_system_action(action)
            else:
                print(f"[ShortcutManager] No action for {page_key}:{btn_name}")
        except Exception as e:
            print(f"[ShortcutManager] Remote press error: {e}")
