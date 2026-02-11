import sys
import os
import json
import importlib.util
import urllib.request

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# Определяем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Добавляем корень проекта в sys.path, чтобы видеть src и resources
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Также добавляем текущую директорию (el_bandito) в sys.path явно, 
# хотя она обычно там есть, но для надежности импортов
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.manager_compile import compile_ui_files, compile_plugin_ui_files

# --- Импорты логики сохранения (Config) ---
try:
    from src.manager_save_load import ConfigManager
except ImportError as e:
    print(f"Ошибка импорта ConfigManager: {e}")
    ConfigManager = None

# --- Импорты логики сервера ---
try:
    from server_thread import ServerThread
except ImportError as e:
    print(f"Ошибка импорта серверных модулей: {e}")
    ServerThread = None

# --- Импорты UI ---
try:
    from resources.ui_done.ui_bandito.ui_el_gui_bandito import Ui_El_GUI_BANDITO
    # Импортируем наш новый класс настроек (напрямую, так как мы в одной папке)
    from el_bandito_setting import BanditoSettings
    from src.manager_plugin import PluginManagerWindow
    from src.plugin_list import PluginListWindow
except ImportError:
    Ui_El_GUI_BANDITO = object 
    BanditoSettings = object
    PluginManagerWindow = object
    PluginListWindow = object

# --- Класс главного окна ---
class BanMainWindow(QMainWindow):
    def __init__(self):
        super(BanMainWindow, self).__init__()
        self.settings_window = None
        self.plugin_manager_window = None
        self.plugin_list_window = None
        self.server_thread = None
        self.current_active_slot = None # Stores the index of the currently active plugin slot
        self.config_manager = ConfigManager(os.path.join(project_root, "configs", "el_bandito_config.json"))
        self.plugin_config_manager = ConfigManager(os.path.join(project_root, "configs", "el_plugin_config.json"))

        # Запускаем сервер автоматически при старте
        self.start_server()

    def start_server(self):
        """Запускает FastAPI сервер в отдельном потоке."""
        if not ServerThread:
            print("ServerThread класс не найден, сервер не запущен.")
            return

        # Читаем настройки
        config = self.config_manager.load_config()
        port = int(config.get("port", 8000))
        # Можно добавить настройку ip_source, но сервер лучше слушать на 0.0.0.0
        
        self.server_thread = ServerThread(host="0.0.0.0", port=port)
        self.server_thread.server_signal.connect(self.on_server_log)
        self.server_thread.start()

    def handle_client_command(self, cmd_data):
        """Обработка команд от клиента (JSON)."""
        print(f"Получена команда: {cmd_data}")
        # Здесь будет логика: если cmd="btn_press" -> выполнить действие
        
        # Обновляем статус в UI сервера, если есть такая возможность
        # Проверим наличие network_stat_line в главном окне
        if hasattr(self.ui, 'network_stat_line'):
             self.ui.network_stat_line.setText(f"CMD: {cmd_data.get('command', '?')}")

    def on_server_log(self, type_msg, data):
        """Обработка логов от сервера."""
        prefix = f"[{type_msg.upper()}] Server:"
        print(f"{prefix} {data}")
        
        if type_msg == "client_connected":
             if hasattr(self.ui, 'network_stat_line'):
                self.ui.network_stat_line.setText(f"Client Connected: {data.get('ip')}")
                self.ui.network_stat_line.setStyleSheet(self.load_style("status_connected"))
        
        elif type_msg == "client_disconnected":
             if hasattr(self.ui, 'network_stat_line'):
                self.ui.network_stat_line.setText("Client Disconnected")
                self.ui.network_stat_line.setStyleSheet(self.load_style("status_disconnected"))

        elif type_msg == "client_switched_slot":
            # Update server UI to reflect client's choice
            index = data.get("index")
            print(f"Client switched to slot {index}")
            # We use set_slot_active to update UI (button state) and load plugin view
            # Pass False to second arg to avoid re-broadcasting if we wanted to avoid loops, 
            # but currently set_slot_active triggers switch_plugin_view which broadcasts.
            # To avoid loop: Client -> Server(Broadcast) -> Client (Done)
            # AND Client -> Server(GUI Update) -> Server(Broadcast) -> Client (Redundant)
            
            # Let's just update UI state without re-triggering logic if possible, or accept redundancy.
            # The cleanest way is to just set the button state visually and load view.
            
            if index is not None:
                self.set_slot_active(index, True)
            else:
                # If index is None, maybe clear?
                pass

        # Если это команда от клиента - обрабатываем
        if type_msg == "command_received":
            self.handle_client_command(data)

    def load_style(self, style_key):
        """Загружает стиль из JSON файла."""
        try:
            import json
            style_path = os.path.join(project_root, "resources", "styles", "style_bandito.json")
            with open(style_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Если запрашивается конкретный ключ
                if style_key in data:
                    style_dict = data.get(style_key, {})
                    css = "; ".join([f"{k}: {v}" for k, v in style_dict.items()])
                    return css
                
                # Иначе возвращаем полный stylesheet
                full_css = ""
                for widget, styles in data.items():
                    if widget.startswith("status_"): continue
                    props = "; ".join([f"{k}: {v}" for k, v in styles.items()])
                    full_css += f"{widget} {{ {props} }} \n"
                return full_css
        except Exception as e:
            print(f"Error loading style: {e}")
            return ""

    def apply_global_styles(self):
        """Применяет глобальные стили к приложению."""
        stylesheet = self.load_style("GLOBAL")
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def closeEvent(self, event):
        """При закрытии окна останавливаем сервер."""
        if self.server_thread and self.server_thread.isRunning():
            print("Остановка сервера...")
            self.server_thread.stop()
            self.server_thread.wait()
        event.accept()

    def setup_logic(self):
        """Здесь подключаем сигналы и слоты после инициализации UI"""
        # Кнопка настроек (settings_toolB)
        if hasattr(self.ui, 'settings_toolB'):
            self.ui.settings_toolB.clicked.connect(self.open_settings)
        else:
            print("Внимание: Кнопка 'settings_toolB' не найдена в UI")

        # Кнопка менеджера плагинов (plugin_toolB)
        if hasattr(self.ui, 'plugin_toolB'):
            self.ui.plugin_toolB.clicked.connect(self.open_plugin_manager)
        else:
            print("Внимание: Кнопка 'plugin_toolB' не найдена в UI")

        # Подключение кнопок добавления плагинов (plugin_add_toolB_1-5)
        for i in range(1, 6):
            # Add
            btn_add_name = f"plugin_add_toolB_{i}"
            if hasattr(self.ui, btn_add_name):
                btn = getattr(self.ui, btn_add_name)
                btn.clicked.connect(lambda checked=False, idx=i: self.open_plugin_list(idx))
            
            # Reload
            btn_reload_name = f"plugin_reload_toolB_{i}"
            if hasattr(self.ui, btn_reload_name):
                btn = getattr(self.ui, btn_reload_name)
                btn.clicked.connect(lambda checked=False, idx=i: self.reload_plugin_slot(idx))

            # Delete
            btn_delete_name = f"plugin_delete_toolB_{i}"
            if hasattr(self.ui, btn_delete_name):
                btn = getattr(self.ui, btn_delete_name)
                btn.clicked.connect(lambda checked=False, idx=i: self.delete_plugin_slot(idx))
            
            # Switch (Select to Show)
            btn_switch_name = f"switch_push_{i}"
            if hasattr(self.ui, btn_switch_name):
                btn = getattr(self.ui, btn_switch_name)
                # Pass checked state to handler
                btn.clicked.connect(lambda checked, idx=i: self.switch_plugin_view(idx))

    def open_settings(self):
        """Открывает окно настроек"""
        if self.settings_window is None:
            self.settings_window = BanditoSettings()
        
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def open_plugin_manager(self):
        """Открывает окно менеджера плагинов"""
        if self.plugin_manager_window is None:
            self.plugin_manager_window = PluginManagerWindow(self)
        
        self.plugin_manager_window.show()

    def open_plugin_list(self, index):
        """Открывает окно списка плагинов (модальное)."""
        print(f"Opening plugin list for slot {index}")
        if self.plugin_list_window is None:
            self.plugin_list_window = PluginListWindow()
            # Подключаем сигнал выбора плагина
            self.plugin_list_window.plugin_selected.connect(self.on_plugin_assigned)
        
        self.plugin_list_window.show_modal(index)

    def update_slot_ui(self, slot_index, plugin_data):
        """Обновляет UI слота информацией о плагине."""
        led_name = f"plugin_led_{slot_index}"
        if hasattr(self.ui, led_name):
            led = getattr(self.ui, led_name)
            if plugin_data:
                display_text = f"{plugin_data.get('name')} v{plugin_data.get('version')}"
                led.setText(display_text)
            else:
                led.setText("")

    def broadcast_plugin_config(self):
        """Отправляет текущую конфигурацию плагинов всем подключенным клиентам."""
        config = self.plugin_config_manager.load_config()
        # Ensure we send safe data
        safe_config = {}
        for k, v in config.items():
            if v:
                safe_config[k] = v
            else:
                safe_config[k] = None
        
        # Broadcast via HTTP to local server
        # We need the port from config
        server_config = self.config_manager.load_config()
        port = int(server_config.get("port", 8000))
        
        try:
            url = f"http://127.0.0.1:{port}/api/broadcast"
            payload = json.dumps({"command": "UPDATE_PLUGIN_SLOTS", "data": safe_config}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                pass
            print("Plugin config broadcasted.")
        except Exception as e:
            print(f"Broadcast failed: {e}")

    def on_plugin_assigned(self, slot_index, plugin_data):
        """Обработчик выбора плагина."""
        print(f"Assigning plugin to slot {slot_index}: {plugin_data}")
        
        # 1. Обновляем UI
        self.update_slot_ui(slot_index, plugin_data)
            
        # 2. Сохраняем в конфиг
        config = self.plugin_config_manager.load_config()
        slot_key = f"slot_{slot_index}"
        config[slot_key] = plugin_data
        self.plugin_config_manager.save_config(config)

        # 3. Automatically turn ON the newly assigned plugin
        self.set_slot_active(slot_index, True)
        
        # 4. Broadcast changes
        self.broadcast_plugin_config()

    def reload_plugin_slot(self, index):
        """Перезагружает метаданные плагина в слоте."""
        print(f"Reloading plugin in slot {index}...")
        
        config = self.plugin_config_manager.load_config()
        slot_key = f"slot_{index}"
        plugin_data = config.get(slot_key)
        
        if not plugin_data:
            print(f"Slot {index} is empty.")
            return

        plugin_dir_name = plugin_data.get("path") or plugin_data.get("id")
        
        plugins_dir = os.path.join(project_root, "plugins")
        plugin_path = os.path.join(plugins_dir, plugin_dir_name)
        
        if not os.path.exists(plugin_path):
            print(f"Plugin directory not found: {plugin_path}")
            return

        # Re-read manifest
        manifest_path = None
        try:
             for f in os.listdir(plugin_path):
                if f.endswith("_manifest.json"):
                    manifest_path = os.path.join(plugin_path, f)
                    break
        except Exception as e:
            print(f"Error searching manifest: {e}")
            return

        if manifest_path:
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Update name
                    plugin_data['name'] = data.get("name", plugin_dir_name)
                    
                    # Update version
                    version_file_rel = data.get("version_file")
                    new_version = "?"
                    if version_file_rel:
                        version_path = os.path.join(project_root, version_file_rel)
                        if os.path.exists(version_path):
                            with open(version_path, 'r', encoding='utf-8') as vf:
                                new_version = vf.read().strip()
                    plugin_data['version'] = new_version
                    
                    # Save back to config
                    config[slot_key] = plugin_data
                    self.plugin_config_manager.save_config(config)
                    
                    # Update UI
                    self.update_slot_ui(index, plugin_data)
                    print(f"Plugin '{plugin_data['name']}' reloaded. Version: {plugin_data['version']}")

            except Exception as e:
                print(f"Error reloading plugin manifest: {e}")

    def delete_plugin_slot(self, index):
        """Удаляет плагин из слота (UI и Config)."""
        print(f"Deleting plugin from slot {index}...")
        
        # 1. Update Config
        config = self.plugin_config_manager.load_config()
        slot_key = f"slot_{index}"
        if slot_key in config:
            config[slot_key] = None
            self.plugin_config_manager.save_config(config)
            print(f"Slot {index} cleared in config.")
            
        # 2. Update UI
        self.update_slot_ui(index, None)
        
        # 3. Disable the slot button
        btn_switch_name = f"switch_push_{index}"
        if hasattr(self.ui, btn_switch_name):
            getattr(self.ui, btn_switch_name).setChecked(False)

        # 4. Clear Right Frame if this slot was active
        if self.current_active_slot == index:
            self.clear_right_frame()
            self.current_active_slot = None
            
        # 5. Broadcast changes
        self.broadcast_plugin_config()

    def broadcast_active_slot(self, index):
        """Отправляет команду переключения активного слота всем клиентам."""
        # Broadcast via HTTP to local server
        server_config = self.config_manager.load_config()
        port = int(server_config.get("port", 8000))
        
        try:
            url = f"http://127.0.0.1:{port}/api/broadcast"
            # index can be None
            payload = json.dumps({
                "command": "SET_ACTIVE_SLOT", 
                "data": {"index": index}
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                pass
            print(f"Active slot {index} broadcasted.")
        except Exception as e:
            print(f"Broadcast active slot failed: {e}")

    def switch_plugin_view(self, index):
        """Переключает видимость плагина в right_frame."""
        btn_switch_name = f"switch_push_{index}"
        if not hasattr(self.ui, btn_switch_name):
            return

        is_checked = getattr(self.ui, btn_switch_name).isChecked()
        print(f"Switching plugin slot {index}. Checked: {is_checked}")

        if is_checked:
            # Turn ON: Load Plugin
            # Uncheck others (Exclusive behavior)
            for i in range(1, 6):
                if i != index:
                     other_btn_name = f"switch_push_{i}"
                     if hasattr(self.ui, other_btn_name):
                         getattr(self.ui, other_btn_name).setChecked(False)
            
            self.load_plugin_ui(index)
            self.current_active_slot = index
            self.broadcast_active_slot(index)
        else:
            # Turn OFF: Unload Plugin if it matches current active
            if self.current_active_slot == index:
                self.clear_right_frame()
                self.current_active_slot = None
                self.broadcast_active_slot(None)

    def set_slot_active(self, index, active=True):
        """Helper to programmatically set slot state."""
        btn_switch_name = f"switch_push_{index}"
        if hasattr(self.ui, btn_switch_name):
            btn = getattr(self.ui, btn_switch_name)
            if btn.isChecked() != active:
                btn.setChecked(active)
                # Manually trigger logic since setChecked doesn't emit clicked
                self.switch_plugin_view(index)

    def load_plugin_ui(self, index):
        """Загружает UI плагина в right_frame (внутренняя логика)."""
        
        # 1. Get plugin data
        config = self.plugin_config_manager.load_config()
        slot_key = f"slot_{index}"
        plugin_data = config.get(slot_key)
        
        if not plugin_data:
            print(f"Slot {index} is empty. Cannot load.")
            self.clear_right_frame()
            # Also uncheck the button since we failed
            btn_switch_name = f"switch_push_{index}"
            if hasattr(self.ui, btn_switch_name):
                getattr(self.ui, btn_switch_name).setChecked(False)
            return
            
        plugin_dir_name = plugin_data.get("path") or plugin_data.get("id")
        plugins_dir = os.path.join(project_root, "plugins")
        plugin_path = os.path.join(plugins_dir, plugin_dir_name)
        
        # 2. Find UI file
        ui_module_path = None
        try:
            for f in os.listdir(plugin_path):
                if f.startswith("ui_") and f.endswith("_bandito.py"):
                    ui_module_path = os.path.join(plugin_path, f)
                    break
        except Exception as e:
            print(f"Error searching UI file: {e}")
            return
            
        if not ui_module_path:
            print(f"UI module not found in {plugin_path}")
            return
            
        # 3. Dynamic Import
        try:
            module_name = f"plugin_ui_{plugin_dir_name}"
            spec = importlib.util.spec_from_file_location(module_name, ui_module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # 4. Instantiate UI class
            ui_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, 'setupUi'):
                     if attr_name.startswith("Ui_"):
                         ui_class = attr
                         break
            
            if not ui_class:
                print("UI class not found in module.")
                return
                
            # 5. Load into right_frame
            self.clear_right_frame()
            
            self.current_plugin_widget = QWidget()
            self.ui_plugin = ui_class()
            self.ui_plugin.setupUi(self.current_plugin_widget)
            
            if not self.ui.right_frame.layout():
                layout = QVBoxLayout(self.ui.right_frame)
                layout.setContentsMargins(0, 0, 0, 0)
                self.ui.right_frame.setLayout(layout)
            
            self.ui.right_frame.layout().addWidget(self.current_plugin_widget)
            print(f"Loaded UI from {ui_module_path}")

        except Exception as e:
            print(f"Error loading plugin UI: {e}")

    def clear_right_frame(self):
        """Очищает содержимое right_frame."""
        if self.ui.right_frame.layout():
            # Remove all items
            while self.ui.right_frame.layout().count():
                item = self.ui.right_frame.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def load_plugin_config(self):
        """Загружает сохраненные плагины в слоты при старте."""
        config = self.plugin_config_manager.load_config()
        if not config:
            return

        first_occupied_slot = None

        for i in range(1, 6):
            slot_key = f"slot_{i}"
            plugin_data = config.get(slot_key)
            if plugin_data:
                self.update_slot_ui(i, plugin_data)
                
                if first_occupied_slot is None:
                    first_occupied_slot = i
        
        # Auto-activate first occupied slot if no slot is active
        if first_occupied_slot is not None and self.current_active_slot is None:
            print(f"Auto-activating slot {first_occupied_slot} on startup")
            # We use set_slot_active which handles button state and logic
            self.set_slot_active(first_occupied_slot, True)


        

def main():
    print("Запуск Server (Bandito)...")
    
    # Настройка путей к ресурсам
    ui_raw_dir = os.path.join(project_root, "resources", "ui_raw")
    ui_done_dir = os.path.join(project_root, "resources", "ui_done")
    
    # Компиляция UI
    print("Проверка UI файлов...")
    compile_ui_files(ui_raw_dir, ui_done_dir)

    # Компиляция Плагинов
    plugins_dir = os.path.join(project_root, "plugins")
    compile_plugin_ui_files(plugins_dir)
    
    # Переимпортируем модули после компиляции
    modules_to_reload = [
        'resources.ui_done.ui_bandito.ui_el_gui_bandito',
        'resources.ui_done.ui_bandito.ui_bandito_settings',
        'el_bandito_setting' # Модуль лежит рядом
    ]
    for mod in modules_to_reload:
        if mod in sys.modules:
            del sys.modules[mod]
    
    try:
        global Ui_El_GUI_BANDITO, BanditoSettings, PluginManagerWindow, PluginListWindow
        from resources.ui_done.ui_bandito.ui_el_gui_bandito import Ui_El_GUI_BANDITO
        from el_bandito_setting import BanditoSettings
        from src.manager_plugin import PluginManagerWindow
        from src.plugin_list import PluginListWindow
    except ImportError as e:
        print(f"Критическая ошибка импорта UI или модулей: {e}")
        sys.exit(1)

    # Запуск QApplication
    app = QApplication(sys.argv)
    
    window = BanMainWindow()
    # Инициализируем UI
    window.ui = Ui_El_GUI_BANDITO()
    window.ui.setupUi(window)
    
    # Применяем глобальные стили
    window.apply_global_styles()
    
    # Подключаем логику
    window.setup_logic()
    
    # Загружаем конфигурацию плагинов
    window.load_plugin_config()
    
    window.show()
    
    print("Сервер запущен.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
