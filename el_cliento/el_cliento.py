import sys
import os

# До любых импортов Qt — иначе не применится
os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.multimedia.*=false")

import json
import importlib.util

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QTimer, QTime

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
    from el_core.el_sound_manager import ElSoundManager
except ImportError as e:
    print(f"Ошибка импорта логики клиента: {e}")
    ConfigManager = None
    BanditoClient = None
    ElSoundManager = None

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
        
        # Инициализация звука
        self.sound_manager = ElSoundManager(self) if ElSoundManager else None
        if self.sound_manager:
            config = self.config_manager.load_config()
            self.sound_manager.set_enabled(config.get("sound_enabled", True))
        
        # Инициализация сокета
        self.socket_client = BanditoClient()
        self.socket_client.log_message.connect(self.on_log)
        self.socket_client.connected.connect(self.on_connected)
        self.socket_client.disconnected.connect(self.on_disconnected)
        self.socket_client.message_received.connect(self._handle_message_received)
        
        self.current_plugin_config = {}
        self.current_active_slot = None
        self._plugin_btn_connections = {}  # slot_index -> QMetaObject.Connection
        self._plugin_instance_cache = {}   # slot_index -> QWidget (Кэш для сохранения state)

        # Timer for real-time clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

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
        # print(f"[Client] {msg}")
        pass
    
    def update_clock(self):
        """Updates HH_lcdN and MM_lcdN with current time."""
        current_time = QTime.currentTime()
        if hasattr(self.ui, 'HH_lcdN'):
            self.ui.HH_lcdN.display(current_time.toString("HH"))
        if hasattr(self.ui, 'MM_lcdN'):
            self.ui.MM_lcdN.display(current_time.toString("mm"))
    
    def _handle_message_received(self, data):
        """Обработка команд от сервера."""
        command = data.get("command")
        
        if command == "UPDATE_PLUGIN_SLOTS":
            # print("[Client] Received plugin config update")
            self.update_plugin_slots(data.get("data", {}))
            
        elif command == "SET_ACTIVE_SLOT":
            slot_index = data.get("data", {}).get("index")
            
            if slot_index == self.current_active_slot:
                # Уже загружено, игнорируем дубликат
                return

            print(f"[Client] Server requested switch to slot {slot_index}")
            
            if slot_index is None:
                # Disable all
                self.clear_right_frame()
                self.current_active_slot = None
            else:
                # Switch to slot if available
                self.load_plugin_ui(slot_index)
                
        elif command == "PLAY_SOUND":
            sound_name = data.get("data", {}).get("name")
            if self.sound_manager and sound_name:
                self.sound_manager.play(sound_name)

        elif command == "UPDATE_SOUND_SETTINGS":
            enabled = data.get("data", {}).get("enabled", True)
            print(f"[Client] Sound settings updated: {enabled}")
            
            # 1. Update main sound manager
            if self.sound_manager:
                self.sound_manager.set_enabled(enabled)
            
            # 2. Update all cached plugin instances
            for slot_idx, instance in self._plugin_instance_cache.items():
                if hasattr(instance, "sound_manager") and instance.sound_manager:
                    instance.sound_manager.set_enabled(enabled)
            
            # 3. Save to local config for persistence
            if self.config_manager:
                # We need to ensure update_config_value exists in ConfigManager or use load/save
                cfg = self.config_manager.load_config()
                cfg["sound_enabled"] = enabled
                self.config_manager.save_config(cfg)

        elif command == "CLIENT_SWITCH_PLUGIN":
             # This command is received from THIS client (echoed back) or another client?
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
                if i in self._plugin_btn_connections:
                    from PySide6.QtCore import QObject
                    QObject.disconnect(self._plugin_btn_connections[i])
                    del self._plugin_btn_connections[i]

                if plugin_data:
                    name = plugin_data.get("name", "Unknown")
                    btn.setText(name)
                    btn.setEnabled(True)
                    conn = btn.clicked.connect(lambda checked=False, idx=i: self.on_plugin_btn_clicked(idx))
                    self._plugin_btn_connections[i] = conn
                    
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
                    if has_plugin:
                        led.setStyleSheet(self.load_style("plugin_inactive"))
                    else:
                        led.setStyleSheet("") # Default style

    def load_plugin_ui(self, index):
        """Загружает UI плагина в right_frame (с использованием QStackedWidget)."""
        # Инициализируем стек при первом вызове
        if not hasattr(self, 'plugin_stack'):
            if not self.ui.right_frame.layout():
                layout = QVBoxLayout(self.ui.right_frame)
                layout.setContentsMargins(0, 0, 0, 0)
                self.ui.right_frame.setLayout(layout)
            
            self.plugin_stack = QStackedWidget()
            self.ui.right_frame.layout().addWidget(self.plugin_stack)
            # Пустая заглушка (индекс 0)
            self.plugin_stack.addWidget(QWidget())

        # 0. Проверяем кэш
        if index in self._plugin_instance_cache:
            instance = self._plugin_instance_cache[index]
            if self.plugin_stack.indexOf(instance) == -1:
                self.plugin_stack.addWidget(instance)
            
            self.plugin_stack.setCurrentWidget(instance)
            self.current_active_slot = index
            self.update_led_indicators(index)
            return

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
        logic_file_name = f"{plugin_dir_name}_cliento.py"
        logic_module_path = os.path.join(plugin_path, logic_file_name)
        
        if os.path.exists(logic_module_path):
            try:
                # ВАЖНО: Добавляем путь плагина в sys.path, только если его там нет
                if plugin_path not in sys.path:
                    sys.path.insert(0, plugin_path)

                module_name = f"client_plugin_logic_{plugin_dir_name}"
                spec = importlib.util.spec_from_file_location(module_name, logic_module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type):
                        if issubclass(attr, QWidget) and not attr_name.startswith("Ui_"):
                             if attr.__module__ == module.__name__:
                                 plugin_class = attr
                                 break
                
                if plugin_class:
                    print(f"[Client] Plugin '{plugin_dir_name}' loaded in slot {index}")
                    
                    # Инстанцируем класс
                    ui_plugin = plugin_class(self.socket_client, plugin_path)
                    
                    # Автоматическая привязка звуков плагина
                    if self.sound_manager:
                        plugin_id = plugin_data.get("id")
                        self.sound_manager.bind_buttons(ui_plugin, context=f"plugin_{plugin_id}")
                    
                    # Кэшируем
                    self._plugin_instance_cache[index] = ui_plugin
                    
                    # Добавляем в стек
                    self.plugin_stack.addWidget(ui_plugin)
                    self.plugin_stack.setCurrentWidget(ui_plugin)
                    
                    self.current_active_slot = index
                    self.update_led_indicators(index)
                    return # Успех
                    
            except Exception as e:
                print(f"[Client] Error loading plugin logic: {e}")

        # --- OLD LOGIC (Fallback): Load pure UI ---
        print("[Client] Fallback to pure UI loading...")
        # ... (код fallback опущен для краткости, аналогично серверу)

    def clear_right_frame(self):
        """Переключает стек на пустой виджет (сохранение state)."""
        self.update_led_indicators(None)
        if hasattr(self, 'plugin_stack'):
            self.plugin_stack.setCurrentIndex(0)
            self.current_active_slot = None

    def load_style(self, style_key):
        """Загружает стиль из JSON файла."""
        try:
            style_path = os.path.join(project_root, "resources", "styles", "style_cliento.json")
            with open(style_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if style_key in data:
                    style_dict = data.get(style_key, {})
                    css = "; ".join([f"{k}: {v}" for k, v in style_dict.items()])
                    return css
                
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
        self.setWindowTitle("El Cliento (Connected)")
        if hasattr(self.ui, 'network_stat_line'):
            self.ui.network_stat_line.setText("Connected")
            self.ui.network_stat_line.setStyleSheet(self.load_style("status_connected"))
        
    def on_disconnected(self):
        self.setWindowTitle("El Cliento (Disconnected)")
        if hasattr(self.ui, 'network_stat_line'):
            self.ui.network_stat_line.setText("Disconnected")
            self.ui.network_stat_line.setStyleSheet(self.load_style("status_disconnected"))

    def setup_logic(self):
        """Здесь подключаем сигналы и слоты после инициализации UI"""
        # Глобальный фильтр для звуков кнопок
        self.installEventFilter(self)

        if hasattr(self.ui, 'settings_toolB'):
            self.ui.settings_toolB.clicked.connect(self.open_settings)

        if hasattr(self.ui, 'full_screen_toolB'):
            self.ui.full_screen_toolB.clicked.connect(self.toggle_fullscreen)
            self.is_fullscreen = False

    def open_settings(self):
        """Открывает окно настроек"""
        if self.settings_window is None:
            self.settings_window = ClientoSettings()
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def toggle_fullscreen(self):
        """Включает/выключает полноэкранный режим"""
        if self.is_fullscreen:
            self.showNormal()
            self.ui.full_screen_toolB.setText("Full Screen")
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.ui.full_screen_toolB.setText("Exit Full Screen")
            self.is_fullscreen = True

    def eventFilter(self, obj, event):
        """Перехват событий для воспроизведения звуков кликов."""
        from PySide6.QtCore import QEvent
        from PySide6.QtWidgets import QPushButton, QToolButton
        
        if event.type() == QEvent.MouseButtonPress:
            if isinstance(obj, (QPushButton, QToolButton)):
                # Глобальный звук теперь управляется через bind_buttons в main()
                # и el_sound_config.json. Убираем принудительный play("click").
                pass
        return super().eventFilter(obj, event)

def main():
    core_updated = cliento_updater.check_and_update()
    try:
        import cliento_plugin_updater
        plugins_updated = cliento_plugin_updater.check_and_update_plugins()
    except Exception as e:
        print(f"Ошибка обновления плагинов: {e}")
        plugins_updated = False

    if core_updated or plugins_updated:
        print("Обновление завершено. Перезапуск...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    try:
        global Ui_El_GUI_CLIENTO, ClientoSettings
        from resources.ui_done.ui_cliento.ui_el_gui_cliento import Ui_El_GUI_CLIENTO
        from cliento_setting import ClientoSettings
    except ImportError as e:
        print(f"Критическая ошибка импорта UI: {e}")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = CliMainWindow()
    window.ui = Ui_El_GUI_CLIENTO()
    window.ui.setupUi(window)
    
    # Загружаем конфиг звуков и привязываем их к кнопкам
    if window.sound_manager:
        sound_cfg_path = os.path.join(project_root, "configs", "el_sound_config.json")
        window.sound_manager.load_config(sound_cfg_path)
        window.sound_manager.bind_buttons(window, "ui_main")
    
    window.apply_global_styles()
    window.setup_logic()
    window.update_clock()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
