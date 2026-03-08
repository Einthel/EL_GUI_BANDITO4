import os
from PySide6.QtWidgets import QDialog, QListWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

try:
    from resources.ui_done.ui_ico_list_di import Ui_ico_list_qW
except ImportError:
    from ..resources.ui_done.ui_ico_list_di import Ui_ico_list_qW

class IcoListDialog(QDialog, Ui_ico_list_qW):
    def __init__(self, parent=None, icon_dir=""):
        super().__init__(parent)
        self.setupUi(self)
        self.icon_dir = icon_dir
        self.selected_icon_path = None
        
        self.load_icons()
        
        self.select_toolB.clicked.connect(self.accept)
        self.cancel_toolB.clicked.connect(self.reject)
        self.ico_listW.itemDoubleClicked.connect(self.accept)

    def load_icons(self):
        if not os.path.exists(self.icon_dir):
            return
            
        extensions = ('.png', '.jpg', '.jpeg', '.ico', '.svg')
        for file_name in os.listdir(self.icon_dir):
            if file_name.lower().endswith(extensions):
                full_path = os.path.join(self.icon_dir, file_name)
                item = QListWidgetItem(file_name)
                item.setIcon(QIcon(full_path))
                item.setData(32, full_path) # Qt.UserRole = 32
                self.ico_listW.addItem(item)

    def get_selected_icon(self):
        current_item = self.ico_listW.currentItem()
        if current_item:
            # Возвращаем относительный путь для сохранения в конфиге
            # Предполагаем, что иконки всегда в resources/ico внутри плагина
            return os.path.join("resources", "ico", current_item.text()).replace("\\", "/")
        return None
