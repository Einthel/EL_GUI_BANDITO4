import os
import sys
from PySide6.QtWidgets import QDialog, QListWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtCore import QFileInfo

# Импорт UI
try:
    from resources.ui_done.ui_app_list_di import Ui_app_list_qW
except ImportError:
    from .resources.ui_done.ui_app_list_di import Ui_app_list_qW

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

        # Инициализация списка для хранения всех приложений
        self.all_apps = []

        # Подключение сигналов поиска
        self.search_lineE.textChanged.connect(self.on_search_text_changed)
        self.search_toolB.clicked.connect(self.on_search_button_clicked)

        # Загрузка списка (в фоне или сразу)
        self.load_applications()

    def load_applications(self):
        """Сканирует папки Start Menu и заполняет список."""
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

        # Сохранение полного списка приложений
        self.all_apps = apps

        # Отображение списка
        self.refresh_list_display(self.all_apps)

    def refresh_list_display(self, apps_to_display):
        """Очищает и перезаполняет список приложений."""
        self.app_listW.clear()

        for name, path in apps_to_display:
            item = QListWidgetItem(name)
            item.setToolTip(path)
            item.setData(Qt.UserRole, path)

            # Получаем иконку
            file_info = QFileInfo(path)
            icon = self.icon_provider.icon(file_info)
            item.setIcon(icon)

            self.app_listW.addItem(item)

    def filter_applications(self, search_text):
        """Фильтрует приложения по поисковому тексту (case-insensitive startswith)."""
        # Если текст пуст, возвращаем все приложения
        if not search_text.strip():
            return self.all_apps

        # Фильтруем приложения: ищем совпадение в начале имени (case-insensitive)
        search_text_lower = search_text.lower()
        filtered_apps = [
            (name, path) for name, path in self.all_apps
            if name.lower().startswith(search_text_lower)
        ]

        return filtered_apps

    def on_search_text_changed(self, text):
        """Обработчик изменения текста в поле поиска (поиск в реальном времени)."""
        filtered_apps = self.filter_applications(text)
        self.refresh_list_display(filtered_apps)

    def on_search_button_clicked(self):
        """Обработчик нажатия кнопки поиска."""
        search_text = self.search_lineE.text()
        filtered_apps = self.filter_applications(search_text)
        self.refresh_list_display(filtered_apps)

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
