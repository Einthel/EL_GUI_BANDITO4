import os
import sys
from PySide6.QtWidgets import QDialog, QListWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtCore import QFileInfo

# Импорт UI
try:
    from ui_app_list_di import Ui_app_list_qW
except ImportError:
    from .ui_app_list_di import Ui_app_list_qW

class AppListDialog(QDialog, Ui_app_list_qW):
    """
    Диалог выбора приложения из меню Пуск.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle("Select Application")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Настройка списка
        self.app_listW.setSelectionMode(QAbstractItemView.SingleSelection)
        self.app_listW.itemSelectionChanged.connect(self.on_selection_changed)
        self.app_listW.itemDoubleClicked.connect(self.accept)
        
        # Икон-провайдер для получения иконок файлов
        self.icon_provider = QFileIconProvider()
        
        # Кнопки
        self.select_toolB.clicked.connect(self.accept)
        self.cancel_toolB.clicked.connect(self.reject)
        self.select_toolB.setEnabled(False)
        
        # Загрузка списка (в фоне или сразу)
        self.load_applications()

    def load_applications(self):
        """Сканирует папки Start Menu и заполняет список."""
        self.app_listW.clear()
        
        # Пути к Start Menu
        paths = [
            os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
        ]
        
        apps = []
        
        for root_path in paths:
            if not os.path.exists(root_path): continue
            
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if file.lower().endswith(".lnk"):
                        name = os.path.splitext(file)[0]
                        full_path = os.path.join(root, file)
                        apps.append((name, full_path))
        
        # Сортировка по имени
        apps.sort(key=lambda x: x[0].lower())
        
        for name, path in apps:
            item = QListWidgetItem(name)
            item.setToolTip(path)
            item.setData(Qt.UserRole, path)
            
            # Получаем иконку
            file_info = QFileInfo(path)
            icon = self.icon_provider.icon(file_info)
            item.setIcon(icon)
            
            self.app_listW.addItem(item)

    def on_selection_changed(self):
        """Активирует кнопку выбора при выделении элемента."""
        self.select_toolB.setEnabled(bool(self.app_listW.selectedItems()))

    def get_selected_app(self):
        """Возвращает (path, name) выбранного приложения."""
        items = self.app_listW.selectedItems()
        if not items:
            return None, None
            
        item = items[0]
        name = item.text()
        path = item.data(Qt.UserRole)
        return path, name
