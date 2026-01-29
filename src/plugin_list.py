import os
import json
from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
from resources.ui_done.ui_plugin_list import Ui_plugin_list_qW

class PluginListWindow(QWidget):
    # Сигнал: номер слота, данные плагина
    plugin_selected = Signal(int, dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window) # Qt.Window ensures it's a window
        self.ui = Ui_plugin_list_qW()
        self.ui.setupUi(self)
        
        self.current_slot_index = -1

        # Make it modal to freeze the parent/main window
        self.setWindowModality(Qt.ApplicationModal)
        
        # Connect cancel button to close
        self.ui.cancel_toolB.clicked.connect(self.close)
        
        # Connect select button
        self.ui.select_toolB.clicked.connect(self.confirm_selection)

        # Determine project root and plugins dir
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(current_dir)
        self.plugins_dir = os.path.join(self.project_root, "plugins")
        self.default_icon_path = os.path.join(self.project_root, "resources", "ico", "ico_add.png")

    def confirm_selection(self):
        """Handle selection and emit signal."""
        selected_items = self.ui.plugin_listW.selectedItems()
        if not selected_items:
            return
            
        item = selected_items[0]
        plugin_data = item.data(Qt.UserRole)
        
        if self.current_slot_index != -1 and plugin_data:
            print(f"Plugin selected for slot {self.current_slot_index}: {plugin_data}")
            self.plugin_selected.emit(self.current_slot_index, plugin_data)
            self.close()

    def load_plugins(self):
        """Scans plugins directory and populates the list widget."""
        self.ui.plugin_listW.clear()
        
        if not os.path.exists(self.plugins_dir):
            print(f"Plugins directory not found: {self.plugins_dir}")
            return
            
        default_icon = QIcon(self.default_icon_path)

        for entry in os.listdir(self.plugins_dir):
            entry_path = os.path.join(self.plugins_dir, entry)
            if os.path.isdir(entry_path):
                if entry == "__pycache__":
                    continue

                # Look for manifest
                manifest_path = None
                # Try to find any file ending with _manifest.json
                try:
                    for f in os.listdir(entry_path):
                        if f.endswith("_manifest.json"):
                            manifest_path = os.path.join(entry_path, f)
                            break
                except OSError:
                    continue
                
                plugin_name = entry
                plugin_id = entry
                plugin_version = "?"
                current_icon = default_icon
                
                if manifest_path:
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            plugin_name = data.get("name", entry)
                            plugin_id = data.get("id", entry)
                            
                            # Read version
                            version_file_rel = data.get("version_file")
                            if version_file_rel:
                                version_path = os.path.join(self.project_root, version_file_rel)
                                if os.path.exists(version_path):
                                    with open(version_path, 'r', encoding='utf-8') as vf:
                                        plugin_version = vf.read().strip()
                            
                            # Read icon
                            icon_file_rel = data.get("icon")
                            if icon_file_rel:
                                icon_path = os.path.join(self.project_root, icon_file_rel)
                                if os.path.exists(icon_path):
                                    current_icon = QIcon(icon_path)

                    except Exception as e:
                        print(f"Error reading manifest/version for {entry}: {e}")
                
                display_text = f"{plugin_name} v{plugin_version}"
                
                # Сохраняем все данные в UserRole
                plugin_data = {
                    "id": plugin_id,
                    "name": plugin_name,
                    "version": plugin_version,
                    "path": entry # имя папки
                }

                item = QListWidgetItem(display_text)
                item.setIcon(current_icon)
                item.setData(Qt.UserRole, plugin_data) # Store ID for later use
                # Tooltip with real folder name
                item.setToolTip(f"ID: {plugin_id}\nFolder: {entry}\nVersion: {plugin_version}")
                self.ui.plugin_listW.addItem(item)

    def show_modal(self, slot_index):
        self.current_slot_index = slot_index
        self.ui.select_toolB.setEnabled(True) # Re-enable if it was disabled
        self.load_plugins() # Refresh list every time window is shown
        self.show()
