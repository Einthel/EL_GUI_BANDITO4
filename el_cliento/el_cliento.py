import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
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

from src.utilts import compile_ui_files

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
    from el_cliento_setting import ClientoSettings
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
    
    # Настройка путей к ресурсам
    ui_raw_dir = os.path.join(project_root, "resources", "ui_raw")
    ui_done_dir = os.path.join(project_root, "resources", "ui_done")
    
    # Компиляция UI
    print("Проверка UI файлов...")
    compile_ui_files(ui_raw_dir, ui_done_dir)
    
    # Переимпортируем модули после компиляции
    modules_to_reload = [
        'resources.ui_done.ui_cliento.ui_el_gui_cliento',
        'resources.ui_done.ui_cliento.ui_cliento_settings',
        'el_cliento_setting'
    ]
    for mod in modules_to_reload:
        if mod in sys.modules:
            del sys.modules[mod]
        
    try:
        global Ui_El_GUI_CLIENTO, ClientoSettings
        from resources.ui_done.ui_cliento.ui_el_gui_cliento import Ui_El_GUI_CLIENTO
        from el_cliento_setting import ClientoSettings
    except ImportError as e:
        print(f"Критическая ошибка импорта UI: {e}")
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
