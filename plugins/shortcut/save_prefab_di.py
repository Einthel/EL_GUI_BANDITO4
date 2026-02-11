from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

# Импорт сгенерированного UI
try:
    from ui_save_prefab_di import Ui_save_prefab_di
except ImportError:
    from .ui_save_prefab_di import Ui_save_prefab_di

class SavePrefabDialog(QDialog, Ui_save_prefab_di):
    """
    Диалог сохранения пресета (префаба) кнопки.
    Позволяет задать уникальное имя для шаблона кнопки.
    """
    def __init__(self, parent=None, default_name=""):
        super().__init__(parent)
        self.setupUi(self)
        
        # Настройка окна
        self.setWindowTitle("Save Preset")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Убираем кнопку "?"
        
        # Предзаполнение имени
        if default_name:
            self.namePrefab_lineE.setText(default_name)
            
        # Подключение сигналов
        self.save_toolB.clicked.connect(self.accept)
        self.cancle_toolB.clicked.connect(self.reject)
        
        # Валидация (опционально)
        self.namePrefab_lineE.textChanged.connect(self.validate_input)
        self.validate_input()

    def validate_input(self):
        """Блокирует кнопку сохранения, если имя пустое."""
        text = self.namePrefab_lineE.text().strip()
        self.save_toolB.setEnabled(bool(text))

    def get_prefab_name(self):
        """Возвращает введенное имя."""
        return self.namePrefab_lineE.text().strip()
