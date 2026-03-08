import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
try:
    from src.tn_cliento_manager import TuneClientoManager
except (ImportError, ValueError):
    from .src.tn_cliento_manager import TuneClientoManager

# Импорт UI
try:
    from resources.ui_done.ui_tune_cliento import Ui_tune_cliento
except ImportError:
    from .resources.ui_done.ui_tune_cliento import Ui_tune_cliento


class TuneClientoPlugin(QWidget, Ui_tune_cliento):
    """Виджет управления звуком с применением стилей и анимаций."""

    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.plugin_path = plugin_path
        self.setupUi(self)
        
        # Инициализация менеджера
        self.manager = TuneClientoManager(socket_client, plugin_path)
        self.manager.style_updated.connect(self.apply_style)
        self.manager.config_updated.connect(self.apply_config)
        
        # Загрузка начальных данных и стилей
        self.manager.load_initial_data()
        
        # Установка фильтра событий для анимаций кнопок
        self.install_event_filter_on_buttons()

    def apply_style(self, css):
        """Применение CSS стиля к виджету."""
        self.setStyleSheet(css)

    def apply_config(self, config: dict):
        """Применение конфигурации аудиоустройств к UI."""
        devices = config.get("output_devices") or []

        first = devices[0] if len(devices) > 0 else ""
        second = devices[1] if len(devices) > 1 else ""

        self.audiD_01_lineE.setText(first)
        self.audiD_02_lineE.setText(second)

        # Подсветка текущего выбранного устройства через dynamic property + stylesheet
        selected = config.get("selected_device") or ""

        # Сбрасываем флаг выбранного устройства
        for lineE in (self.audiD_01_lineE, self.audiD_02_lineE):
            lineE.setProperty("selectedDevice", False)

        # Помечаем активную строку
        if selected and selected == first:
            self.audiD_01_lineE.setProperty("selectedDevice", True)
        elif selected and selected == second:
            self.audiD_02_lineE.setProperty("selectedDevice", True)

        # Обновляем стили для применения CSS по dynamic property
        for lineE in (self.audiD_01_lineE, self.audiD_02_lineE):
            lineE.style().unpolish(lineE)
            lineE.style().polish(lineE)
            lineE.update()

    def install_event_filter_on_buttons(self):
        """Установка фильтра событий на все кнопки для анимации."""
        for button in self.findChildren(QWidget):
            if hasattr(button, 'clicked'):
                button.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Централизованная обработка нажатий и анимаций."""
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.MouseButtonPress:
            self.animate_click(obj)
            # Отправка команды через менеджер, если у объекта есть имя (ID)
            if obj.objectName():
                self.manager.send_button_press(obj.objectName())
        return super().eventFilter(obj, event)

    def animate_click(self, widget):
        """Анимация нажатия (масштабирование)."""
        self.animation = QPropertyAnimation(widget, b"geometry")
        self.animation.setDuration(100)
        self.animation.setStartValue(widget.geometry())
        
        # Небольшое уменьшение
        rect = widget.geometry()
        shrink_rect = rect.adjusted(2, 2, -2, -2)
        self.animation.setKeyValueAt(0.5, shrink_rect)
        self.animation.setEndValue(rect)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
