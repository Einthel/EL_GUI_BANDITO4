import os
import sys
import importlib.util
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from .el_state_manager import ElStateManager
from .el_com_manager import ElComManager
from .el_sound_manager import ElSoundManager

class ElCore(QObject):
    """
    Оркестратор (Core).
    Связывает состояние (State), коммуникации (Com) и логику плагинов.
    Является единственной точкой входа для UI сервера.
    """
    
    # --- Сигналы для UI ---
    log_message = Signal(str, str)          # type, msg
    slot_config_updated = Signal(int, dict) # slot_index, plugin_data (когда изменился конфиг слота)
    active_slot_changed = Signal(int)       # slot_index (когда сменился активный плагин)
    plugin_view_loaded = Signal(QWidget)    # widget (готовый UI плагина для вставки в окно)

    def __init__(self, config_path, project_root):
        super().__init__()
        self.project_root = project_root
        
        # Инициализация менеджеров
        self.state = ElStateManager(config_path)
        self.com = ElComManager()
        self.sound = ElSoundManager(self)
        
        # Загрузка настроек звука
        sound_cfg_path = os.path.join(self.project_root, "configs", "el_sound_config.json")
        self.sound.load_config(sound_cfg_path)
        
        # Загрузка настроек звука СЕРВЕРА из правильного конфига
        bandito_cfg_path = os.path.join(self.project_root, "configs", "el_bandito_config.json")
        if os.path.exists(bandito_cfg_path):
            from src.manager_save_load import ConfigManager
            server_config = ConfigManager(bandito_cfg_path).load_config()
            self.sound.set_enabled(server_config.get("sound_enabled", True))
        else:
            self.sound.set_enabled(True)
        
        # Подключение сигналов от ComManager
        self.com.log_message.connect(self.log_message)
        self.com.command_received.connect(self._handle_client_command)
        self.com.client_switched_slot.connect(self._on_client_switched_slot)
        self.com.client_connected.connect(self._on_client_connected)
        self.com.client_disconnected.connect(self._on_client_disconnected)
        
        # Автозапуск сервера
        self.com.start_service()

    def stop(self):
        """Остановка ядра и сервисов."""
        self.com.stop_service()

    def set_sound_enabled(self, enabled: bool):
        """
        Обновляет настройки звука КЛИЕНТА:
        1. Сохраняет в конфиг клиента (el_cliento_config.json).
        2. Оповещает клиентов.
        """
        cliento_cfg_path = os.path.abspath(os.path.join(self.project_root, "configs", "el_cliento_config.json"))
        print(f"[Core] Saving CLIENT sound setting to: {cliento_cfg_path}")
        self.state.update_config_value("sound_enabled", enabled, custom_path=cliento_cfg_path)
        
        self.com.broadcast("UPDATE_SOUND_SETTINGS", {"enabled": enabled})
        self.log_message.emit("info", f"Client sound {'enabled' if enabled else 'disabled'}")

    def set_server_sound_enabled(self, enabled: bool):
        """
        Обновляет настройки звука СЕРВЕРА:
        1. Сохраняет в конфиг сервера (el_bandito_config.json).
        2. Применяет на сервере.
        """
        # Сохраняем в основной конфиг сервера
        bandito_cfg_path = os.path.abspath(os.path.join(self.project_root, "configs", "el_bandito_config.json"))
        print(f"[Core] Saving SERVER sound setting to: {bandito_cfg_path}")
        self.state.update_config_value("sound_enabled", enabled, custom_path=bandito_cfg_path)
        
        self.sound.set_enabled(enabled)
        self.log_message.emit("info", f"Server sound {'enabled' if enabled else 'disabled'}")

    # --- Управление слотами (API для UI) ---

    def assign_plugin(self, slot_index: int, plugin_data: dict):
        """
        Назначает плагин на слот.
        """
        # Очищаем старый инстанс из кэша при смене плагина
        self.state.clear_plugin_instance(slot_index)
        
        self.state.update_slot(slot_index, plugin_data)
        
        # Broadcast safe config (remove None values if needed, but clients handle nulls)
        self.com.broadcast("UPDATE_PLUGIN_SLOTS", self.state.get_all_slots())
        
        self.slot_config_updated.emit(slot_index, plugin_data)
        self.log_message.emit("info", f"Plugin assigned to slot {slot_index}")

        # Авто-активация, если это первый плагин
        if self.state.get_active_slot() is None and plugin_data:
            self.activate_slot(slot_index)

    def remove_plugin(self, slot_index: int):
        """Удаляет плагин из слота."""
        self.assign_plugin(slot_index, None)
        
        # Если удалили активный плагин - сбрасываем активность
        if self.state.get_active_slot() == slot_index:
            self.activate_slot(None)

    def activate_slot(self, slot_index: int):
        """
        Активирует слот (переключает плагин).
        1. Обновляет State.
        2. Отправляет команду клиентам.
        3. Загружает логику и UI плагина.
        """
        # Проверка на избыточность: если слот уже активен, ничего не делаем
        if slot_index == self.state.get_active_slot():
            return

        # Если index None - деактивация
        if slot_index is None:
            self.state.set_active_slot(None)
            self.com.broadcast("SET_ACTIVE_SLOT", {"index": None})
            self.active_slot_changed.emit(None) # UI должен очистить фрейм
            return

        plugin_data = self.state.get_slot(slot_index)
        if not plugin_data:
            self.log_message.emit("warning", f"Cannot activate empty slot {slot_index}")
            return

        # 1. Update State
        self.state.set_active_slot(slot_index)
        
        # 2. Broadcast
        self.com.broadcast("SET_ACTIVE_SLOT", {"index": slot_index})
        #self.com.broadcast("PLAY_SOUND", {"name": "click"}) # Звук переключения для всех клиентов
        self.active_slot_changed.emit(slot_index)
        
        # Локальный звук на сервере
        #self.sound.play("click")
        
        # 3. Load Logic & UI
        try:
            plugin_widget = self._load_plugin_instance(slot_index, plugin_data)
            if plugin_widget:
                self.plugin_view_loaded.emit(plugin_widget)
        except Exception as e:
            self.log_message.emit("error", f"Failed to load plugin: {e}")

    # --- Внутренняя логика загрузки плагинов ---

    def _load_plugin_instance(self, slot_index, plugin_data):
        """
        Загружает модуль плагина, создает экземпляр класса и возвращает виджет.
        Кэширует экземпляр в StateManager.
        """
        existing_instance = self.state.get_plugin_instance(slot_index)
        if existing_instance:
            return existing_instance

        plugin_dir_name = plugin_data.get("path") or plugin_data.get("id")
        plugins_dir = os.path.join(self.project_root, "plugins")
        plugin_path = os.path.join(plugins_dir, plugin_dir_name)

        # Поиск класса логики (Server Plugin Class)
        logic_file_name = f"{plugin_dir_name}_bandito.py"
        logic_module_path = os.path.join(plugin_path, logic_file_name)
        
        plugin_class = None
        
        if os.path.exists(logic_module_path):
            try:
                # Оптимизация: добавляем путь только если его еще нет в sys.path
                if plugin_path not in sys.path:
                    sys.path.insert(0, plugin_path)
                    
                logic_mod_name = f"server_plugin_class_{plugin_dir_name}"
                spec = importlib.util.spec_from_file_location(logic_mod_name, logic_module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[logic_mod_name] = module
                spec.loader.exec_module(module)
                
                # Ищем класс наследник QWidget
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, QWidget) and attr.__module__ == module.__name__:
                        plugin_class = attr
                        break
            except Exception as e:
                self.log_message.emit("error", f"Error loading plugin logic class: {e}")

        # Инстанцирование (plugin_path+core → plugin_path → без аргументов)
        widget = None
        if plugin_class:
            try:
                widget = plugin_class(plugin_path, core=self)
            except TypeError:
                try:
                    widget = plugin_class(plugin_path)
                except TypeError:
                    widget = plugin_class()
            
            # Автоматическая привязка звуков плагина
            if widget and self.sound:
                plugin_id = plugin_data.get("id")
                self.sound.bind_buttons(widget, context=f"plugin_{plugin_id}")
            
            # Кэшируем (для обработки команд)
            self.state.cache_plugin_instance(slot_index, widget)
            
        else:
            # Fallback: Чистый UI (без логики обработки команд)
            widget = self._load_pure_ui(plugin_path, plugin_dir_name)
            # В этом случае кэшируем None или widget, но он не обработает команды
            self.state.cache_plugin_instance(slot_index, widget)

        return widget

    def _load_pure_ui(self, plugin_path, plugin_dir_name):
        """Загрузка UI из скомпилированного файла (Fallback)."""
        ui_module_path = None
        ui_done_path = os.path.join(plugin_path, "resources", "ui_done")
        
        if os.path.exists(ui_done_path):
            for f in os.listdir(ui_done_path):
                if f.startswith("ui_") and f.endswith("_bandito.py"):
                    ui_module_path = os.path.join(ui_done_path, f)
                    break
        
        if not ui_module_path:
            return None

        try:
            module_name = f"plugin_ui_{plugin_dir_name}"
            spec = importlib.util.spec_from_file_location(module_name, ui_module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            ui_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, 'setupUi') and attr_name.startswith("Ui_"):
                    ui_class = attr
                    break
            
            if ui_class:
                container = QWidget()
                ui = ui_class()
                ui.setupUi(container)
                return container
        except Exception as e:
            self.log_message.emit("error", f"Error loading pure UI: {e}")
        
        return None

    # --- Обработка событий ---

    def _handle_client_command(self, cmd_data):
        """Обработка команд от клиента."""
        command = cmd_data.get("command")
        if command == "PLUGIN_BUTTON_PRESS":
            active_idx = self.state.get_active_slot()
            if active_idx:
                instance = self.state.get_plugin_instance(active_idx)
                if instance and hasattr(instance, "handle_button_press"):
                    payload = cmd_data.get("payload", {})
                    btn_id = payload.get("id")
                    print(f"[Core] PLUGIN_BUTTON_PRESS → slot {active_idx} '{btn_id}'")
                    try:
                        instance.handle_button_press(btn_id, None) # path уже внутри instance
                    except Exception as e:
                        self.log_message.emit("error", f"Plugin execution error: {e}")
                else:
                    self.log_message.emit("warning", f"Active plugin {active_idx} cannot handle button press")

    def _on_client_switched_slot(self, index):
        """Клиент сам переключил слот."""
        self.log_message.emit("info", f"Client switched to slot {index}")
        self.activate_slot(index)

    def _on_client_connected(self, data):
        self.state.add_client(data.get("ip"))

    def _on_client_disconnected(self, data):
        self.state.remove_client(data.get("ip"))

    def get_initial_config(self):
        """Возвращает конфиг для начальной инициализации UI."""
        return self.state.get_all_slots()
