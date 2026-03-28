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

        # Подключение слайдеров
        if hasattr(self, "sound_volume_slider"):
            # Используем sliderMoved для мгновенного отклика (если сервер справится)
            # или оставляем sliderReleased для надежности
            self.sound_volume_slider.sliderReleased.connect(self._on_sound_slider_released)
        if hasattr(self, "mic_volume_slider"):
            self.mic_volume_slider.sliderReleased.connect(self._on_mic_slider_released)

    def _on_sound_slider_released(self):
        """Отправка нового значения громкости звука на сервер."""
        val = self.sound_volume_slider.value()
        self.manager.send_volume_change("sound_volume_slider", val)

    def _on_mic_slider_released(self):
        """Отправка нового значения громкости микрофона на сервер."""
        val = self.mic_volume_slider.value()
        self.manager.send_volume_change("mic_volume_slider", val)

    def apply_style(self, css):
        """Применение CSS стиля к виджету."""
        self.setStyleSheet(css)

    def apply_config(self, config: dict):
        """Применение конфигурации аудиоустройств к UI."""
        devices = config.get("output_devices") or []
        active_devices = config.get("active_devices") or []

        first = devices[0] if len(devices) > 0 else ""
        second = devices[1] if len(devices) > 1 else ""
        bt_device = config.get("selected_bt_device") or ""

        self.audiD_01_lineE.setText(first)
        self.audiD_02_lineE.setText(second)
        self.bt_audiD_lineE.setText(bt_device)
        self.mic_01_lineE.setText(config.get("selected_mic") or "")

        # Обновление кнопки мута микрофона на клиенте
        is_mic_muted = config.get("input_devices_muted", False)
        mic_mute_btn = getattr(self, "mic_mute_toolB", None)
        if mic_mute_btn:
            mic_mute_btn.blockSignals(True)
            mic_mute_btn.setChecked(is_mic_muted)
            mic_mute_btn.setText("Muted" if is_mic_muted else "Mute")
            mic_mute_btn.setProperty("isMuted", is_mic_muted)
            mic_mute_btn.style().unpolish(mic_mute_btn)
            mic_mute_btn.style().polish(mic_mute_btn)
            mic_mute_btn.update()
            mic_mute_btn.blockSignals(False)

        # Обновление кнопки мута звука на клиенте
        is_sound_muted = config.get("output_devices_muted", False)
        sound_mute_btn = getattr(self, "sound_mute_toolB", None)
        if sound_mute_btn:
            sound_mute_btn.blockSignals(True)
            sound_mute_btn.setChecked(is_sound_muted)
            sound_mute_btn.setText("Muted" if is_sound_muted else "Sound")
            sound_mute_btn.setProperty("isMuted", is_sound_muted)
            sound_mute_btn.style().unpolish(sound_mute_btn)
            sound_mute_btn.style().polish(sound_mute_btn)
            sound_mute_btn.update()
            sound_mute_btn.blockSignals(False)

        # Обновление слайдеров громкости
        sound_vol = config.get("output_devices_volume")
        if sound_vol is not None and hasattr(self, "sound_volume_slider"):
            self.sound_volume_slider.blockSignals(True)
            self.sound_volume_slider.setValue(int(sound_vol))
            self.sound_volume_slider.blockSignals(False)

        mic_vol = config.get("input_devices_volume")
        if mic_vol is not None and hasattr(self, "mic_volume_slider"):
            self.mic_volume_slider.blockSignals(True)
            self.mic_volume_slider.setValue(int(mic_vol))
            self.mic_volume_slider.blockSignals(False)

        # Блокировка недоступных устройств
        # (Кортеж: Поле ввода, Кнопка переключения, Название устройства)
        device_widgets = [
            (self.audiD_01_lineE, self.audiD_01_toolB, first),
            (self.audiD_02_lineE, self.audiD_02_toolB, second),
            (self.bt_audiD_lineE, self.bt_audiD_toolB, bt_device)
        ]

        for lineE, toolB, name in device_widgets:
            # Устройство активно, если его имя есть в списке active_devices
            is_active = name in active_devices if name else False
            lineE.setEnabled(is_active)
            if toolB:
                toolB.setEnabled(is_active)

        # Подсветка текущего выбранного устройства через dynamic property + stylesheet
        selected = config.get("selected_device") or ""

        # Сбрасываем флаг выбранного устройства
        for lineE in (self.audiD_01_lineE, self.audiD_02_lineE, self.bt_audiD_lineE):
            lineE.setProperty("selectedDevice", False)

        # Помечаем активную строку
        if selected:
            if selected == first:
                self.audiD_01_lineE.setProperty("selectedDevice", True)
            elif selected == second:
                self.audiD_02_lineE.setProperty("selectedDevice", True)
            elif selected == bt_device:
                self.bt_audiD_lineE.setProperty("selectedDevice", True)

        # Обновляем стили для применения CSS по dynamic property
        for lineE in (self.audiD_01_lineE, self.audiD_02_lineE, self.bt_audiD_lineE, self.mic_01_lineE):
            lineE.style().unpolish(lineE)
            lineE.style().polish(lineE)
            lineE.update()

    def install_event_filter_on_buttons(self):
        """Установка фильтра событий на все кнопки для анимации."""
        from PySide6.QtWidgets import QAbstractButton
        # Находим только реальные кнопки (QPushButton, QToolButton и т.д.)
        for button in self.findChildren(QAbstractButton):
            button.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Централизованная обработка нажатий и анимаций."""
        from PySide6.QtCore import QEvent
        from PySide6.QtWidgets import QSlider
        if event.type() == QEvent.MouseButtonPress:
            # Игнорируем слайдеры в общем фильтре нажатий кнопок
            if isinstance(obj, QSlider):
                return super().eventFilter(obj, event)
                
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
