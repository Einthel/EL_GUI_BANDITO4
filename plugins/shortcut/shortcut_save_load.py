import os
from src.manager_save_load import ConfigManager

class ShortcutDataManager:
    def __init__(self, plugin_path):
        self.plugin_path = plugin_path
        # Путь к файлу конфига
        config_path = os.path.join(plugin_path, "config", "button_shortcut.json")
        # Инициализируем низкоуровневый менеджер
        self.config_manager = ConfigManager(config_path)
        # Загружаем данные в память
        self.data = self.config_manager.load_config()
        
        # Менеджер для префабов
        prefab_path = os.path.join(plugin_path, "config", "prefab_but_shortcut.json")
        self.prefab_manager = ConfigManager(prefab_path)
        self.prefabs = self.prefab_manager.load_config()
        if "prefabs" not in self.prefabs:
            self.prefabs["prefabs"] = {}

    def get_data(self):
        """Возвращает текущий словарь данных."""
        return self.data

    def get_prefabs(self):
        """Возвращает словарь префабов."""
        return self.prefabs.get("prefabs", {})

    def save_prefab(self, name, btn_data):
        """Сохраняет префаб кнопки."""
        if "prefabs" not in self.prefabs:
            self.prefabs["prefabs"] = {}
            
        self.prefabs["prefabs"][name] = btn_data
        self.prefab_manager.save_config(self.prefabs)
        print(f"[ShortcutDataManager] Prefab saved: {name}")

    def delete_prefab(self, name):
        """Удаляет префаб."""
        if "prefabs" in self.prefabs and name in self.prefabs["prefabs"]:
            del self.prefabs["prefabs"][name]
            self.prefab_manager.save_config(self.prefabs)
            print(f"[ShortcutDataManager] Prefab deleted: {name}")

    def rename_prefab(self, old_name, new_name):
        """Переименовывает префаб."""
        if "prefabs" in self.prefabs and old_name in self.prefabs["prefabs"]:
            # Берем данные старого
            data = self.prefabs["prefabs"].pop(old_name)
            # Сохраняем с новым именем
            self.prefabs["prefabs"][new_name] = data
            self.prefab_manager.save_config(self.prefabs)
            print(f"[ShortcutDataManager] Prefab renamed: {old_name} -> {new_name}")

    def save(self):
        """Сохраняет текущее состояние данных в файл."""
        self.config_manager.save_config(self.data)

    def add_new_page(self):
        """Создает новую страницу с следующим порядковым индексом."""
        max_index = 0
        for key in self.data.keys():
            if key.startswith("page_"):
                try:
                    idx = int(key.split("_")[1])
                    if idx > max_index: max_index = idx
                except ValueError:
                    continue
        
        new_index = max_index + 1
        new_key = f"page_{new_index}"
        self.data[new_key] = {}
        self.save()
        return new_index

    def remove_page(self, current_page_index):
        """
        Удаляет страницу по индексу и сдвигает индексы остальных.
        Возвращает скорректированный индекс страницы (чтобы UI знал, куда переключиться).
        """
        # Считаем количество страниц
        page_keys = [k for k in self.data.keys() if k.startswith("page_")]
        if len(page_keys) <= 1:
            print("[ShortcutDataManager] Cannot remove the last page.")
            return current_page_index

        current_key = f"page_{current_page_index}"
        
        # Удаляем текущую страницу
        if current_key in self.data:
            del self.data[current_key]
            print(f"[ShortcutDataManager] Removed page: {current_key}")
            
            # Переиндексация страниц (сдвиг вниз)
            # Находим все страницы с индексом БОЛЬШЕ текущего
            pages_to_shift = []
            for key in list(self.data.keys()):
                 if key.startswith("page_"):
                    try:
                        idx = int(key.split("_")[1])
                        if idx > current_page_index:
                            pages_to_shift.append((key, idx))
                    except ValueError:
                        continue
            
            # Сортируем по возрастанию индекса, чтобы корректно переименовывать
            pages_to_shift.sort(key=lambda x: x[1])
            
            for old_key, old_idx in pages_to_shift:
                new_idx = old_idx - 1
                new_key = f"page_{new_idx}"
                # Перемещаем данные из старого ключа в новый
                self.data[new_key] = self.data.pop(old_key)
                print(f"[ShortcutDataManager] Shifted {old_key} -> {new_key}")

            # Корректируем текущий индекс
            # Если мы удалили последнюю страницу, нужно уменьшить индекс
            # Проверяем, существует ли страница с текущим индексом
            if f"page_{current_page_index}" not in self.data:
                 current_page_index -= 1
            
            if current_page_index < 1:
                current_page_index = 1
                
            self.save()
            return current_page_index
        else:
            return current_page_index

    def update_button(self, page_index, btn_id, btn_data):
        """Обновляет или создает данные для конкретной кнопки."""
        page_key = f"page_{page_index}"
        if page_key not in self.data:
            self.data[page_key] = {}
        
        self.data[page_key][btn_id] = btn_data
        self.save()

    def delete_button(self, page_index, btn_id):
        """Удаляет данные кнопки."""
        page_key = f"page_{page_index}"
        if page_key in self.data and btn_id in self.data[page_key]:
            del self.data[page_key][btn_id]
            self.save()
            print(f"[ShortcutDataManager] Deleted config for {btn_id} on page {page_index}")
