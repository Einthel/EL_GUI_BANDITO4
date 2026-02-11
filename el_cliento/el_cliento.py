import sys
import os
import json
import importlib.util

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# Определяем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Добавляем корень проекта в sys.path, чтобы видеть src
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Добавляем текущую директорию в path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Импорт апдейтера
import cliento_updater

# --- Импорты логики ---
try:
    from src.manager_save_load import ConfigManager
    from cliento_socket import BanditoClient
except ImportError as e:
    print(f"Ошибка импорта логики клиента: {e}")
    ConfigManager = None
    BanditoClient = None

# --- Импорты UI ---
try:
    from resources.ui_done.ui_cliento.ui_el_gui_cliento import Ui_El_GUI_CLIENTO
    # Импортируем наш новый класс настроек
    from cliento_setting import ClientoSettings
except ImportError:
    Ui_El_GUI_CLIENTO = object
    ClientoSettings = object

# --- Класс главного окна ---
class CliMainWindow(QMainWindow):
    def __init__(self):
        super(CliMainWindow, self).__init__()
        self.settings_window = None
        self.config_manager = ConfigManager(os.path.join(project_root, "configs", "el_cliento_config.json"))
        
        # Инициализация сокета
        self.socket_client = BanditoClient()
        self.socket_client.log_message.connect(self.on_log)
        self.socket_client.connected.connect(self.on_connected)
        self.socket_client.disconnected.connect(self.on_disconnected)
        self.socket_client.message_received.connect(self.on_message_received)
        
        self.current_plugin_config = {}
        self.current_active_slot = None
        
        # Пробуем подключиться при старте
        self.init_connection()

    def init_connection(self):
        """Читает настройки и запускает подключение."""
        config = self.config_manager.load_config()
        ip = config.get("ip_destination", "127.0.0.1")
        port = config.get("port", "8000")
        
        if ip and port:
            self.socket_client.set_connection_info(ip, port)
            self.socket_client.connect_to_server()
        else:
            print("Нет настроек подключения (IP/Port)")

    def on_log(self, msg):
        print(f"[Client] {msg}")
    
    def on_message_received(self, data):
        """Обработка команд от сервера."""
        command = data.get("command")
        
        if command == "UPDATE_PLUGIN_SLOTS":
            print("[Client] Received plugin config update")
            self.update_plugin_slots(data.get("data", {}))
            
        elif command == "SET_ACTIVE_SLOT":
            slot_index = data.get("data", {}).get("index")
            print(f"[Client] Server requested switch to slot {slot_index}")
            
            if slot_index is None:
                # Disable all
                self.clear_right_frame()
                self.current_active_slot = None
            else:
                # Switch to slot if available
                self.load_plugin_ui(slot_index)
                
        elif command == "CLIENT_SWITCH_PLUGIN":
             # This command is received from THIS client (echoed back) or another client?
             # Actually, if client switches plugin, it should tell server, and server tells everyone including this client.
             # But here we are listening to server.
             pass

    def update_plugin_slots(self, slots_data):
        """Обновляет UI кнопок плагинов и сохраняет конфигурацию."""
        self.current_plugin_config = slots_data
        
        first_occupied_slot = None

        for i in range(1, 6):
            slot_key = f"slot_{i}"
            plugin_data = slots_data.get(slot_key)
            
            btn_name = f"plugin_toolB_{i}"
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                
                # Disconnect previous connections to avoid duplicates
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                
                if plugin_data:
                    name = plugin_data.get("name", "Unknown")
                    btn.setText(name)
                    btn.setEnabled(True)
                    # Connect click
                    # When client clicks, we just load UI locally AND tell server
                    btn.clicked.connect(lambda checked=False, idx=i: self.on_plugin_btn_clicked(idx))
                    
                    if first_occupied_slot is None:
                        first_occupied_slot = i
                else:
                    btn.setText("Empty")
                    btn.setEnabled(False)
                    # If this slot was active, clear it
                    if self.current_active_slot == i:
                        self.clear_right_frame()
                        self.current_active_slot = None

        # Auto-select the first occupied slot if no slot is active
        if first_occupied_slot is not None and self.current_active_slot is None:
            print(f"[Client] Auto-selecting slot {first_occupied_slot}")
            self.load_plugin_ui(first_occupied_slot)

    def on_plugin_btn_clicked(self, index):
        """Called when user clicks a plugin button on client."""
        # 1. Load locally (optimistic update)
        self.load_plugin_ui(index)
        
        # 2. Tell server to switch active slot
        self.socket_client.send_command("CLIENT_SET_ACTIVE_SLOT", {"index": index})

    def update_led_indicators(self, active_index):
        """Updates style for plugin LED indicators."""
        for i in range(1, 6):
            led_name = f"plugin_led_lineE_{i}"
            if hasattr(self.ui, led_name):
                led = getattr(self.ui, led_name)
                
                # Check if this slot has a plugin assigned
                slot_key = f"slot_{i}"
                has_plugin = bool(self.current_plugin_config.get(slot_key))
                
                if i == active_index and has_plugin:
                    led.setStyleSheet(self.load_style("plugin_active"))
                else:
                    # You can set different styles for empty vs inactive but populated
                    if has_plugin:
                        led.setStyleSheet(self.load_style("plugin_inactive"))
                    else:
                        led.setStyleSheet("") # Default style

    def load_plugin_ui(self, index):
        """Загружает UI плагина в right_frame."""
        print(f"[Client] Loading plugin for slot {index}...")
        
        slot_key = f"slot_{index}"
        plugin_data = self.current_plugin_config.get(slot_key)
        
        if not plugin_data:
            print("No data for slot")
            self.update_led_indicators(None)
            return

        plugin_dir_name = plugin_data.get("path") or plugin_data.get("id")
        plugins_dir = os.path.join(project_root, "plugins")
        plugin_path = os.path.join(plugins_dir, plugin_dir_name)
        
        # --- NEW LOGIC: Try to load Plugin Logic Class first ---
        # Ищем файл логики: <plugin_dir_name>_cliento.py
        logic_file_name = f"{plugin_dir_name}_cliento.py"
        logic_module_path = os.path.join(plugin_path, logic_file_name)
        
        if os.path.exists(logic_module_path):
            print(f"[Client] Found logic module: {logic_module_path}")
            try:
                # ВАЖНО: Добавляем путь плагина в sys.path, чтобы импорты внутри него работали
                # Мы делаем это временно или постоянно? Постоянно не страшно.
                if plugin_path not in sys.path:
                    sys.path.insert(0, plugin_path)

                module_name = f"client_plugin_logic_{plugin_dir_name}"
                spec = importlib.util.spec_from_file_location(module_name, logic_module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Ищем класс, который наследуется от QWidget (но не Ui_...)
                # Обычно мы договоримся называть его MainClass или как-то похоже
                # Или просто искать класс с __init__, принимающий socket_client
                
                # Эвристика: ищем класс, имя которого заканчивается на "Plugin" или "Client"
                # И который НЕ начинается на Ui_
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    # Check if it is a class
                    if isinstance(attr, type):
                        # Check inheritance and name
                        if issubclass(attr, QWidget) and not attr_name.startswith("Ui_"):
                             # CRITICAL: Check if the class is defined IN THIS MODULE
                             # Imports like QToolButton will have __module__ like 'PySide6.QtWidgets'
                             # We only want classes defined in the loaded module
                             if attr.__module__ == module.__name__:
                                 plugin_class = attr
                                 break
                
                if plugin_class:
                    print(f"[Client] Instantiating plugin logic class: {plugin_class.__name__}")
                    self.clear_right_frame()
                    
                    # Инстанцируем класс, передавая socket_client и путь
                    # Важно: класс должен принимать эти аргументы
                    self.ui_plugin = plugin_class(self.socket_client, plugin_path)
                    
                    # Добавляем в UI
                    if not self.ui.right_frame.layout():
                        layout = QVBoxLayout(self.ui.right_frame)
                        layout.setContentsMargins(0, 0, 0, 0)
                        self.ui.right_frame.setLayout(layout)
                    
                    self.ui.right_frame.layout().addWidget(self.ui_plugin)
                    
                    self.current_active_slot = index
                    self.update_led_indicators(index)
                    return # Успех, выходим
                    
            except Exception as e:
                print(f"[Client] Error loading plugin logic: {e}")
                # Если ошибка - пробуем фоллбэк на старый метод (только UI)

        # --- OLD LOGIC (Fallback): Load pure UI ---
        print("[Client] Fallback to pure UI loading...")
        # Find UI file: ui_*_cliento.py
        ui_module_path = None
        try:
            if os.path.exists(plugin_path):
                for f in os.listdir(plugin_path):
                    if f.startswith("ui_") and f.endswith("_cliento.py"):
                        ui_module_path = os.path.join(plugin_path, f)
                        break
        except Exception as e:
            print(f"Error searching UI file: {e}")
            return
            
        if not ui_module_path:
            print(f"UI module not found in {plugin_path}")
            return
            
        # Dynamic Import
        try:
            module_name = f"client_plugin_ui_{plugin_dir_name}"
            spec = importlib.util.spec_from_file_location(module_name, ui_module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Find UI class
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
                
            # Load into right_frame
            self.clear_right_frame()
            
            self.current_plugin_widget = QWidget()
            self.ui_plugin = ui_class()
            self.ui_plugin.setupUi(self.current_plugin_widget)
            
            if not self.ui.right_frame.layout():
                layout = QVBoxLayout(self.ui.right_frame)
                layout.setContentsMargins(0, 0, 0, 0)
                self.ui.right_frame.setLayout(layout)
            
            self.ui.right_frame.layout().addWidget(self.current_plugin_widget)
            print(f"Loaded Plugin UI from {ui_module_path}")
            self.current_active_slot = index
            
            # Update LEDs
            self.update_led_indicators(index)

        except Exception as e:
            print(f"Error loading plugin UI: {e}")

    def clear_right_frame(self):
        """Очищает содержимое right_frame."""
        # Also clear LED selection
        self.update_led_indicators(None)
        
        if self.ui.right_frame.layout():
            while self.ui.right_frame.layout().count():
                item = self.ui.right_frame.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def load_style(self, style_key):
        """Загружает стиль из JSON файла."""
        try:
            import json
            style_path = os.path.join(project_root, "resources", "styles", "style_cliento.json")
            with open(style_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Если запрашивается конкретный ключ (например, статус)
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

    def on_connected(self):
        # Меняем заголовок или цвет, чтобы показать коннект
        self.setWindowTitle("El Cliento (Connected)")
        # Индикатор сети в UI (если есть)
        if hasattr(self.ui, 'network_stat_line'):
            self.ui.network_stat_line.setText("Connected")
            self.ui.network_stat_line.setStyleSheet(self.load_style("status_connected"))
        
    def on_disconnected(self):
        self.setWindowTitle("El Cliento (Disconnected)")
        # Индикатор сети в UI
        if hasattr(self.ui, 'network_stat_line'):
            self.ui.network_stat_line.setText("Disconnected")
            self.ui.network_stat_line.setStyleSheet(self.load_style("status_disconnected"))

    def setup_logic(self):
        """Здесь подключаем сигналы и слоты после инициализации UI"""
        # Кнопка настроек (settings_toolB)
        if hasattr(self.ui, 'settings_toolB'):
            self.ui.settings_toolB.clicked.connect(self.open_settings)
        else:
            print("Внимание: Кнопка 'settings_toolB' не найдена в UI клиента")
            
        # Тестовая привязка всех кнопок (для примера)
        # Ищем все кнопки в UI, начинающиеся на 'btn_' или 'toolButton_'
        # В реальном проекте тут будет логика биндинга конкретных кнопок
        for widget in self.findChildren(QWidget):
            name = widget.objectName()
            # Простой пример: если имя кнопки содержит "btn", шлем команду
            # (нужно уточнить реальные имена кнопок в UI)
            if "btn" in name.lower() or "toolB" in name: 
                # Исключаем кнопку настроек
                if name == "settings_toolB": continue
                
                try:
                    # Используем lambda с capture переменной name
                    # widget.clicked.connect(lambda checked=False, n=name: self.send_btn_press(n))
                    # Для надежности лучше использовать отдельный метод-слот, но пока так
                    pass 
                except:
                    pass

    def send_btn_press(self, btn_name):
        """Отправка нажатия кнопки на сервер."""
        self.socket_client.send_command("btn_press", {"id": btn_name})

    def open_settings(self):
        """Открывает окно настроек"""
        if self.settings_window is None:
            self.settings_window = ClientoSettings()
        
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

def main():
    print("Запуск Client (Cliento)...")
    
    # --- БЛОК ОБНОВЛЕНИЯ ---
    print("Проверка обновлений ядра...")
    core_updated = cliento_updater.check_and_update()
    
    print("Проверка обновлений плагинов...")
    try:
        import cliento_plugin_updater
        plugins_updated = cliento_plugin_updater.check_and_update_plugins()
    except Exception as e:
        print(f"Ошибка обновления плагинов: {e}")
        plugins_updated = False

    if core_updated or plugins_updated:
        print("Обновление завершено. Перезапуск...")
        # Перезапускаем текущий скрипт
        python = sys.executable
        os.execl(python, python, *sys.argv)
    # -----------------------

    # Настройка путей к ресурсам
    # (Компиляция удалена, используем готовые файлы с сервера)

    try:
        global Ui_El_GUI_CLIENTO, ClientoSettings
        from resources.ui_done.ui_cliento.ui_el_gui_cliento import Ui_El_GUI_CLIENTO
        from cliento_setting import ClientoSettings
    except ImportError as e:
        print(f"Критическая ошибка импорта UI: {e}")
        print("Возможно, файлы UI не были загружены апдейтером.")
        sys.exit(1)
    
    # Запуск приложения
    app = QApplication(sys.argv)
    
    window = CliMainWindow()
    window.ui = Ui_El_GUI_CLIENTO()
    window.ui.setupUi(window)
    
    # Применяем глобальные стили
    window.apply_global_styles()
    
    # Подключаем логику
    window.setup_logic()
    
    # window.showFullScreen() 
    window.show()
    
    print("Клиент запущен.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
