import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
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

from src.utilts import compile_ui_files

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
except ImportError:
    Ui_El_GUI_BANDITO = object 
    BanditoSettings = object
    PluginManagerWindow = object

# --- Класс главного окна ---
class BanMainWindow(QMainWindow):
    def __init__(self):
        super(BanMainWindow, self).__init__()
        self.settings_window = None
        self.plugin_manager_window = None
        self.server_thread = None
        self.config_manager = ConfigManager(os.path.join(project_root, "configs", "el_bandito_config.json"))

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

        

def main():
    print("Запуск Server (Bandito)...")
    
    # Настройка путей к ресурсам
    ui_raw_dir = os.path.join(project_root, "resources", "ui_raw")
    ui_done_dir = os.path.join(project_root, "resources", "ui_done")
    
    # Компиляция UI
    print("Проверка UI файлов...")
    compile_ui_files(ui_raw_dir, ui_done_dir)
    
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
        global Ui_El_GUI_BANDITO, BanditoSettings, PluginManagerWindow
        from resources.ui_done.ui_bandito.ui_el_gui_bandito import Ui_El_GUI_BANDITO
        from el_bandito_setting import BanditoSettings
        from src.manager_plugin import PluginManagerWindow
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
    
    window.show()
    
    print("Сервер запущен.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
