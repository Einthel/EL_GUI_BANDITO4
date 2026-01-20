from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from resources.ui_done.ui_plugin_manager import Ui_plugin_manager_qW

class PluginManagerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_plugin_manager_qW()
        self.ui.setupUi(self)
        
        # Устанавливаем модальность окна, чтобы блокировать основное окно
        self.setWindowModality(Qt.ApplicationModal)
