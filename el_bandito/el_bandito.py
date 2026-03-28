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

# Также добавляем текущую директорию (el_bandito) в sys.path явно
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.manager_compile import compile_ui_files, compile_plugin_ui_files

# --- Импорты логики сохранения (Config) ---
try:
    from src.manager_save_load import ConfigManager
except ImportError as e:
    print(f"Ошибка импорта ConfigManager: {e}")
    ConfigManager = None

# --- Импорт ElCore (Оркестратор) ---
try:
    from el_core.el_core import ElCore
except ImportError as e:
    print(f"Ошибка импорта ElCore: {e}")
    ElCore = None

# --- Импорты UI ---
try:
    from resources.ui_done.ui_bandito.ui_el_gui_bandito import Ui_El_GUI_BANDITO
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
        
        self.config_manager = ConfigManager(os.path.join(project_root, "configs", "el_bandito_config.json"))
        
        # Инициализация Core
        self.core = None
        if ElCore:
            plugin_config_path = os.path.join(project_root, "configs", "el_plugin_config.json")
            self.core = ElCore(plugin_config_path, project_root)
            
            # Подключение сигналов Core
            self.core.log_message.connect(self.on_log)
            self.core.slot_config_updated.connect(self.update_slot_ui)
            self.core.active_slot_changed.connect(self.on_core_active_slot_changed)
            self.core.plugin_view_loaded.connect(self.show_plugin_view)
            
            # Подключение сетевых статусов
            self.core.com.client_connected.connect(lambda data: self.on_log("info", f"Client connected: {data.get('ip')}"))
            self.core.com.client_disconnected.connect(self.on_client_disconnected)

    def _enrich_slot_data_from_manifest(self, slot_index):
        """Возвращает plugin_data с гарантированными name и version (из манифеста при отсутствии)."""
        data = self.core.state.get_slot(slot_index) if self.core else None
        if not data or not isinstance(data, dict):
            return data
        path = data.get("path") or data.get("id")
        if not path:
            return data
        name = data.get("name")
        version = data.get("version")
        if name and version:
            return data
        plugins_dir = os.path.join(project_root, "plugins")
        manifest_path = os.path.join(plugins_dir, path)
        try:
            for f in os.listdir(manifest_path):
                if f.endswith("_manifest.json"):
                    manifest_path = os.path.join(manifest_path, f)
                    break
            else:
                return data
            if not os.path.isfile(manifest_path):
                return data
            with open(manifest_path, "r", encoding="utf-8") as f:
                m = json.load(f)
            out = dict(data)
            if not name:
                out["name"] = m.get("name", path)
            if not version:
                if manifest_path.endswith(".json"):
                    out["version"] = m.get("min_app_version", "?")
                else:
                    out["version"] = "?"
            return out
        except Exception:
            return data

    def _init_ui_from_core(self):
        """Заполняет UI на основе начального состояния Core."""
        for i in range(1, 6):
            data = self._enrich_slot_data_from_manifest(i)
            self.update_slot_ui(i, data)

        # Восстанавливаем активный слот из конфига
        initial_slots = self.core.get_initial_config()
        first_occupied = None
        for i in range(1, 6):
            if initial_slots.get(f"slot_{i}"):
                first_occupied = i
                break
        
        if first_occupied is not None:
            # print(f"Auto-activating slot {first_occupied} on startup")  # DEBUG
            # Используем QTimer, чтобы UI успел полностью инициализироваться
            from PySide6.QtCore import QTimer
            QTimer.singleShot(100, lambda: self.core.activate_slot(first_occupied))

    def on_log(self, type_msg, msg):
        """Обработка логов от Core."""
        # print(f"[{type_msg.upper()}] Core: {msg}")  # DEBUG: полный вывод
        if "Client connected" in msg:
            ip = msg.split(": ")[-1] if ": " in msg else "?"
            print(f"[Core] Client: {ip}")
        elif "Client disconnected" in msg:
            ip = msg.split(": ")[-1] if ": " in msg else "?"
            print(f"[Core] Disconnect: {ip}")
        else:
            print(f"[Core] {msg}")

        # Обновление статуса сети в UI
        if "Client connected" in msg:
             if hasattr(self.ui, 'network_stat_line'):
                self.ui.network_stat_line.setText(msg)
                self.ui.network_stat_line.setStyleSheet(self.load_style("status_connected"))
        elif "Client disconnected" in msg:
             if hasattr(self.ui, 'network_stat_line'):
                self.ui.network_stat_line.setText("Client Disconnected")
                self.ui.network_stat_line.setStyleSheet(self.load_style("status_disconnected"))

    def on_client_disconnected(self, data):
        """Обработка отключения клиента."""
        ip = data.get("ip", "Unknown")
        if hasattr(self.ui, 'network_stat_line'):
            self.ui.network_stat_line.setText(f"Disconnected: {ip}")
            self.ui.network_stat_line.setStyleSheet(self.load_style("status_disconnected"))

    def load_style(self, style_key):
        """Loads style from JSON file (Material Design)."""
        try:
            path = os.path.join(project_root, "resources", "styles", "style_bn_material.json")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if style_key in data:
                return "; ".join([f"{k}: {v}" for k, v in data[style_key].items()])
            
            # Construct global stylesheet
            css = ""
            for selector, props in data.items():
                # Skip metadata and manual-only status styles
                if selector.startswith(("__", "animation", "status_", "plugin_active", "plugin_inactive")): 
                    continue
                
                props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                css += f"{selector} {{ {props_str} }}\n"
            return css
        except Exception as e:
            print(f"Style Load Error: {e}")
            return ""

    def apply_global_styles(self):
        """Применяет глобальные стили к приложению."""
        stylesheet = self.load_style("GLOBAL")
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def closeEvent(self, event):
        """При закрытии окна останавливаем Core."""
        if self.core:
            print("Остановка Core...")
            self.core.stop()
        event.accept()

    def setup_logic(self):
        """Здесь подключаем сигналы и слоты после инициализации UI"""
        # Кнопка настроек
        if hasattr(self.ui, 'settings_toolB'):
            self.ui.settings_toolB.clicked.connect(self.open_settings)

        # Кнопка менеджера плагинов
        if hasattr(self.ui, 'plugin_toolB'):
            self.ui.plugin_toolB.clicked.connect(self.open_plugin_manager)

        # Подключение кнопок управления слотами
        for i in range(1, 6):
            # Add
            btn_add_name = f"plugin_add_toolB_{i}"
            if hasattr(self.ui, btn_add_name):
                getattr(self.ui, btn_add_name).clicked.connect(lambda checked=False, idx=i: self.open_plugin_list(idx))
            
            # Reload
            btn_reload_name = f"plugin_reload_toolB_{i}"
            if hasattr(self.ui, btn_reload_name):
                getattr(self.ui, btn_reload_name).clicked.connect(lambda checked=False, idx=i: self.reload_plugin_slot(idx))

            # Delete
            btn_delete_name = f"plugin_delete_toolB_{i}"
            if hasattr(self.ui, btn_delete_name):
                getattr(self.ui, btn_delete_name).clicked.connect(lambda checked=False, idx=i: self.delete_plugin_slot(idx))
            
            # Switch (Select to Show)
            btn_switch_name = f"switch_push_{i}"
            if hasattr(self.ui, btn_switch_name):
                getattr(self.ui, btn_switch_name).clicked.connect(lambda checked, idx=i: self.switch_plugin_view(idx))

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = BanditoSettings(self.core)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def open_plugin_manager(self):
        if self.plugin_manager_window is None:
            self.plugin_manager_window = PluginManagerWindow(self)
        self.plugin_manager_window.show()

    def open_plugin_list(self, index):
        print(f"Opening plugin list for slot {index}")
        if self.plugin_list_window is None:
            self.plugin_list_window = PluginListWindow()
            self.plugin_list_window.plugin_selected.connect(self.on_plugin_assigned)
        self.plugin_list_window.show_modal(index)

    def on_plugin_assigned(self, slot_index, plugin_data):
        """Callback от списка плагинов -> Core."""
        if self.core:
            self.core.assign_plugin(slot_index, plugin_data)

    def delete_plugin_slot(self, index):
        """Удаление плагина -> Core."""
        if self.core:
            self.core.remove_plugin(index)

    def switch_plugin_view(self, index):
        """Переключение вида (кнопка нажата пользователем)."""
        btn_switch_name = f"switch_push_{index}"
        if not hasattr(self.ui, btn_switch_name): return

        is_checked = getattr(self.ui, btn_switch_name).isChecked()
        
        if self.core:
            if is_checked:
                self.core.activate_slot(index)
            else:
                # Если отжали кнопку активного слота -> деактивация
                # Но нужно проверить, был ли он активен
                if self.core.state.get_active_slot() == index:
                    self.core.activate_slot(None)

    def reload_plugin_slot(self, index):
        """Перезагрузка метаданных (UI Logic -> Core Update)."""
        # Логика чтения манифеста оставлена в UI слое для простоты, 
        # но обновление состояния идет через Core.
        if not self.core: return
        
        plugin_data = self.core.state.get_slot(index)
        if not plugin_data: return

        plugin_dir_name = plugin_data.get("path") or plugin_data.get("id")
        plugins_dir = os.path.join(project_root, "plugins")
        plugin_path = os.path.join(plugins_dir, plugin_dir_name)
        
        manifest_path = None
        try:
             for f in os.listdir(plugin_path):
                if f.endswith("_manifest.json"):
                    manifest_path = os.path.join(plugin_path, f)
                    break
        except Exception: pass

        if manifest_path:
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    plugin_data['name'] = data.get("name", plugin_dir_name)
                    
                    # Read version
                    version_file_rel = data.get("version_file")
                    new_version = "?"
                    if version_file_rel:
                        version_path = os.path.join(project_root, version_file_rel)
                        if os.path.exists(version_path):
                            try:
                                with open(version_path, 'r', encoding='utf-8') as vf:
                                    content = vf.read().strip()
                                    if version_file_rel.endswith(".json"):
                                        v_data = json.loads(content)
                                        new_version = v_data.get("min_app_version", "?")
                                    else:
                                        new_version = content
                            except Exception as e:
                                print(f"Error parsing version file: {e}")
                    plugin_data['version'] = new_version
                    
                    # Update via Core
                    self.core.assign_plugin(index, plugin_data)
                    print(f"Plugin reloaded: {plugin_data['name']} v{plugin_data['version']}")
            except Exception as e:
                print(f"Error reloading manifest: {e}")

    # --- UI Update Slots (Called by Core Signals) ---

    def update_slot_ui(self, slot_index, plugin_data):
        """Обновляет текст на LED индикаторах (название и версия плагина)."""
        if not getattr(self, "ui", None):
            return
        if plugin_data and isinstance(plugin_data, dict) and (not plugin_data.get("name") or not plugin_data.get("version")):
            plugin_data = self._enrich_slot_data_from_manifest(slot_index) or plugin_data
        led_name = f"plugin_led_{slot_index}"
        if hasattr(self.ui, led_name):
            led = getattr(self.ui, led_name)
            if plugin_data and isinstance(plugin_data, dict):
                name = plugin_data.get("name") or "?"
                version = plugin_data.get("version") or "?"
                led.setText(f"{name} v{version}")
            else:
                led.setText("")
        
        # Если плагин удален, отжимаем кнопку
        if not plugin_data:
            btn_switch_name = f"switch_push_{slot_index}"
            if hasattr(self.ui, btn_switch_name):
                getattr(self.ui, btn_switch_name).setChecked(False)

    def on_core_active_slot_changed(self, active_index):
        """Обновляет состояние кнопок переключения (вызывается сигналом Core)."""
        print(f"[UI] Active slot changed to: {active_index}")
        # Сбрасываем все кнопки
        for i in range(1, 6):
            btn_name = f"switch_push_{i}"
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                # Блокируем сигналы, чтобы не вызвать рекурсию switch_plugin_view
                btn.blockSignals(True)
                btn.setChecked(i == active_index)
                btn.blockSignals(False)
        
        if active_index is None:
            self.clear_right_frame()

    def show_plugin_view(self, widget):
        """Отображает виджет плагина в right_frame через QStackedWidget."""
        if not self.ui.right_frame.layout():
            from PySide6.QtWidgets import QStackedWidget
            layout = QVBoxLayout(self.ui.right_frame)
            layout.setContentsMargins(0, 0, 0, 0)
            self.stack = QStackedWidget()
            layout.addWidget(self.stack)
            # Добавляем пустой виджет как заглушку (индекс 0)
            self.stack.addWidget(QWidget())
        
        # Если виджета еще нет в стеке - добавляем
        if self.stack.indexOf(widget) == -1:
            self.stack.addWidget(widget)
        
        self.stack.setCurrentWidget(widget)

    def clear_right_frame(self):
        """Переключает стек на пустой виджет (сохраняя плагины в памяти)."""
        if hasattr(self, 'stack'):
            self.stack.setCurrentIndex(0)

def main():
    print("Запуск Server (Bandito)...")
    
    # Настройка путей к ресурсам
    ui_raw_dir = os.path.join(project_root, "resources", "ui_raw")
    ui_done_dir = os.path.join(project_root, "resources", "ui_done")
    
    # Компиляция UI
    compile_ui_files(ui_raw_dir, ui_done_dir)
    plugins_dir = os.path.join(project_root, "plugins")
    compile_plugin_ui_files(plugins_dir)
    print("Проверка UI файлов: ok")
    
    # Переимпортируем модули после компиляции
    modules_to_reload = [
        'resources.ui_done.ui_bandito.ui_el_gui_bandito',
        'resources.ui_done.ui_bandito.ui_bandito_settings',
        'el_bandito_setting'
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
    window._init_ui_from_core()

    # Привязываем звуки к кнопкам основного интерфейса
    if window.core and window.core.sound:
        window.core.sound.bind_buttons(window, "ui_main")
    
    # Применяем глобальные стили
    window.apply_global_styles()
    
    # Подключаем логику UI
    window.setup_logic()
    
    window.show()
    
    print("Server: Online")
    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Server: Error — {e}")
        raise

if __name__ == "__main__":
    main()
