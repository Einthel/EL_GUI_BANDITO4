import sys
import os

# Определяем путь к корню проекта для импорта модулей из src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.manager_save_load import ConfigManager
except ImportError as e:
    print(f"[ElStateManager] Error importing ConfigManager: {e}")
    ConfigManager = None

class ElStateManager:
    """
    Центральное хранилище состояния системы (RAM + JSON Persistence).
    Отвечает за:
    1. Хранение конфигурации слотов (какой плагин где).
    2. Хранение текущего активного слота (runtime).
    3. Кэширование загруженных объектов плагинов.
    4. Отслеживание подключенных клиентов.
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_manager = ConfigManager(config_path) if ConfigManager else None
        
        # --- State Data ---
        self.slots = {}          # {1: plugin_data, 2: None, ...}
        self.active_slot = None  # int index or None
        self.loaded_plugins = {} # {index: plugin_instance}
        self.connected_clients = set() # Set of client identifiers (e.g., IP:Port)
        
        # Инициализация
        self._init_empty_slots()
        self.load_state()

    def _init_empty_slots(self):
        """Создает пустую структуру слотов."""
        for i in range(1, 6):
            self.slots[i] = None

    def load_state(self):
        """Загружает конфигурацию слотов из JSON."""
        if not self.config_manager:
            print("[ElStateManager] State loaded: error — ConfigManager not initialized.")
            return

        data = self.config_manager.load_config()
        if data is None:
            print("[ElStateManager] State loaded: error — config read failed.")
            return

        for i in range(1, 6):
            key = f"slot_{i}"
            self.slots[i] = data.get(key)
        
        # print(f"[ElStateManager] State loaded from {self.config_path}")  # DEBUG
        print("[ElStateManager] State loaded: ok")

    def save_state(self):
        """Сохраняет текущую конфигурацию слотов в JSON."""
        if not self.config_manager:
            return

        data = {}
        for i, plugin_data in self.slots.items():
            data[f"slot_{i}"] = plugin_data
        
        self.config_manager.save_config(data)
        # print("[ElStateManager] State saved.")

    def update_config_value(self, key: str, value, custom_path: str = None):
        """
        Обновляет произвольное значение в конфиге и сохраняет его.
        :param key: Ключ в JSON
        :param value: Значение
        :param custom_path: Опциональный путь к другому JSON файлу
        """
        manager = self.config_manager
        if custom_path:
            if not os.path.exists(custom_path):
                print(f"[ElStateManager] ERROR: Target config file not found: {custom_path}")
                return
            try:
                manager = ConfigManager(custom_path)
            except Exception as e:
                print(f"[ElStateManager] Error creating manager for {custom_path}: {e}")
                return

        if not manager:
            return

        config = manager.load_config()
        config[key] = value
        manager.save_config(config)
        print(f"[ElStateManager] Config updated ({os.path.basename(manager.file_path) if manager else 'unknown'}): {key} = {value}")

    # --- Slot Management ---

    def update_slot(self, index: int, plugin_data: dict):
        """
        Обновляет данные плагина в слоте и сохраняет конфиг.
        :param index: Номер слота (1-5)
        :param plugin_data: Словарь с данными плагина или None (для очистки)
        """
        if index not in self.slots:
            print(f"[ElStateManager] Invalid slot index: {index}")
            return

        self.slots[index] = plugin_data
        self.save_state()

    def get_slot(self, index: int):
        """Возвращает данные плагина для слота."""
        return self.slots.get(index)

    def get_all_slots(self):
        """Возвращает копию всех слотов (для broadcast)."""
        # Преобразуем ключи в строки "slot_N" для совместимости с клиентом
        result = {}
        for i, data in self.slots.items():
            result[f"slot_{i}"] = data
        return result

    # --- Active Slot Management ---

    def set_active_slot(self, index: int):
        """Устанавливает текущий активный слот (только в RAM)."""
        self.active_slot = index

    def get_active_slot(self):
        """Возвращает индекс активного слота."""
        return self.active_slot

    # --- Plugin Instance Cache ---

    def cache_plugin_instance(self, index: int, instance):
        """Сохраняет экземпляр класса плагина."""
        self.loaded_plugins[index] = instance

    def get_plugin_instance(self, index: int):
        """Возвращает сохраненный экземпляр плагина."""
        return self.loaded_plugins.get(index)

    def clear_plugin_instance(self, index: int):
        """Удаляет экземпляр плагина из кэша (например, при перезагрузке)."""
        if index in self.loaded_plugins:
            del self.loaded_plugins[index]

    # --- Client Tracking ---

    def add_client(self, client_id):
        """Регистрирует подключение клиента."""
        self.connected_clients.add(client_id)
        # print(f"[ElStateManager] Client connected: {client_id}. Total: {len(self.connected_clients)}")  # DEBUG

    def remove_client(self, client_id):
        """Регистрирует отключение клиента."""
        if client_id in self.connected_clients:
            self.connected_clients.remove(client_id)
            # print(f"[ElStateManager] Client disconnected: {client_id}. Total: {len(self.connected_clients)}")  # DEBUG

    def get_clients(self):
        """Возвращает список подключенных клиентов."""
        return list(self.connected_clients)
