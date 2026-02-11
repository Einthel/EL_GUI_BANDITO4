from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

# Импорт сгенерированного UI
try:
    from ui_questions_di import Ui_questions_di
except ImportError:
    from .ui_questions_di import Ui_questions_di

class QuestionsDialog(QDialog, Ui_questions_di):
    """
    Универсальный диалог вопроса (Да/Нет).
    """
    def __init__(self, parent=None, question_text="Are you sure?"):
        super().__init__(parent)
        self.setupUi(self)
        
        # Настройка окна
        self.setWindowTitle("Question")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Установка текста вопроса
        self.questions_lable.setText(question_text)
        
        # Подключение сигналов
        self.yes_toolB.clicked.connect(self.accept)
        self.no_toolB.clicked.connect(self.reject)
