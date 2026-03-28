import os
import json
from PySide6.QtWidgets import QWidget, QToolButton, QGridLayout, QFrame, QGraphicsOpacityEffect
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QEvent, QRect, QSize

# Импорты сервисов и менеджера
try:
    from .src.sh_cliento_service import (
        load_config, load_style_data, parse_style_to_css, 
        load_anim_config
    )
    from .src.sh_cliento_manager import ShortcutClientManager
except ImportError:
    from src.sh_cliento_service import (
        load_config, load_style_data, parse_style_to_css, 
        load_anim_config
    )
    from src.sh_cliento_manager import ShortcutClientManager

try:
    from resources.ui_done.ui_shortcut_cliento import Ui_stream_cliento
except ImportError:
    from .resources.ui_done.ui_shortcut_cliento import Ui_stream_cliento

class ShortcutClientPlugin(QWidget, Ui_stream_cliento):
    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.plugin_path = plugin_path
        
        # Инициализация звука
        from el_core.el_sound_manager import ElSoundManager
        self.sound_manager = ElSoundManager(self)
        
        # Загрузка конфига звуков (как на сервере)
        sound_cfg_path = os.path.join(os.path.dirname(os.path.dirname(self.plugin_path)), "configs", "el_sound_config.json")
        self.sound_manager.load_config(sound_cfg_path)
        
        # Load current sound state from client config
        try:
            from src.manager_save_load import ConfigManager
            cliento_cfg_path = os.path.join(os.path.dirname(os.path.dirname(self.plugin_path)), "configs", "el_cliento_config.json")
            if os.path.exists(cliento_cfg_path):
                cliento_cfg = ConfigManager(cliento_cfg_path).load_config()
                self.sound_manager.set_enabled(cliento_cfg.get("sound_enabled", True))
        except Exception as e:
            print(f"[ShortcutPlugin] Error loading sound config: {e}")
        
        # Инициализация менеджера
        self.manager = ShortcutClientManager(socket_client, plugin_path)
        self.manager.config_updated.connect(self._handle_config_updated)
        self.manager.page_change_requested.connect(self.handle_page_change)
        
        # Инициализация UI
        self.setupUi(self)
        
        # Загрузка данных
        self.anim_config = load_anim_config(self.plugin_path)
        self.active_animations = {}
        
        # Применение стилей и конфига
        self.apply_plugin_styles()
        self.manager.set_config(load_config(self.plugin_path))
        
        # Настройка кнопок
        self.setup_buttons()
        
        # Применяем эффекты Elevation
        for btn in self.findChildren(QToolButton):
            if btn.property("applyShadow"):
                self.apply_elevation(btn)
        
        # Подписка на сокет через менеджер
        if socket_client:
            socket_client.message_received.connect(self.manager.on_server_message)

    def apply_plugin_styles(self):
        """Загружает и применяет стили."""
        # Новые стили Material 2
        style_path = os.path.join(self.plugin_path, "config", "style_sh_cl_material.json")
        
        # Старые стили (закомментированы)
        # style_path = os.path.join(self.plugin_path, "config", "style_shortcut_cliento.json")
        
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)
                if style_data:
                    css = parse_style_to_css(style_data)
                    self.setStyleSheet(css)
            except Exception as e:
                print(f"[ShortcutCliento] Error loading style: {e}")

    def apply_elevation(self, widget):
        """Применяет эффект тени (Elevation) к виджету."""
        if not widget.property("applyShadow"):
            return
            
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        from PySide6.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 150))
        widget.setGraphicsEffect(shadow)

    def eventFilter(self, watched, event):
        """Анимация кнопок."""
        if isinstance(watched, QToolButton):
            if event.type() == QEvent.MouseButtonPress:
                self.animate_button(watched, True)
            elif event.type() == QEvent.MouseButtonRelease:
                self.animate_button(watched, False)
                # Хак для сброса hover-эффекта на тачскринах
                watched.setAttribute(Qt.WA_UnderMouse, False)
                watched.update()
            elif event.type() == QEvent.Leave:
                self.animate_button(watched, False)
                watched.setAttribute(Qt.WA_UnderMouse, False)
                watched.update()
        return super().eventFilter(watched, event)

    def animate_button(self, btn, pressed):
        """Логика анимации масштабирования."""
        if not hasattr(btn, 'original_geometry'):
            btn.original_geometry = btn.geometry()

        if btn in self.active_animations:
            self.active_animations[btn].stop()

        anim = QPropertyAnimation(btn, b"geometry")
        anim.setDuration(self.anim_config.get("duration", 100))
        
        curve_name = self.anim_config.get("easing_curve", "OutQuad")
        anim.setEasingCurve(getattr(QEasingCurve, curve_name, QEasingCurve.OutQuad))

        orig = btn.original_geometry
        if pressed:
            factor = self.anim_config.get("scale_factor", 0.95)
            new_w, new_h = orig.width() * factor, orig.height() * factor
            new_x = orig.x() + (orig.width() - new_w) / 2
            new_y = orig.y() + (orig.height() - new_h) / 2
            end_geo = QRect(new_x, new_y, new_w, new_h)
        else:
            end_geo = orig

        anim.setStartValue(btn.geometry())
        anim.setEndValue(end_geo)
        self.active_animations[btn] = anim
        anim.start()

    def _handle_config_updated(self, new_config):
        """Реакция на обновление конфига от менеджера."""
        self.clear_ui()
        self.setup_buttons()

    def handle_page_change(self, direction):
        """Навигация по страницам."""
        # 1. Сбрасываем состояние фокуса и hover для всех кнопок текущей страницы перед переключением
        current_page = self.Button_stackedWidget.currentWidget()
        if current_page:
            for btn in current_page.findChildren(QToolButton):
                btn.clearFocus()
                btn.setAttribute(Qt.WA_UnderMouse, False)
                btn.update()

        # 2. Переключаем страницу
        if direction == "next":
            self.next_page()
        elif direction == "prev":
            self.prev_page()

        # 3. Принудительно сбрасываем состояние hover для всех кнопок на новой странице
        # Это решает проблему, когда курсор оказывается над кнопкой на новой странице сразу после переключения
        new_page = self.Button_stackedWidget.currentWidget()
        if new_page:
            for btn in new_page.findChildren(QToolButton):
                btn.setAttribute(Qt.WA_UnderMouse, False)
                btn.clearFocus()
                btn.update()

    def clear_ui(self):
        """Очистка StackedWidget."""
        while self.Button_stackedWidget.count() > 0:
            widget = self.Button_stackedWidget.widget(0)
            self.Button_stackedWidget.removeWidget(widget)
            widget.deleteLater()

    def setup_buttons(self):
        """Построение UI кнопок на основе конфига менеджера."""
        existing_pages = {self.Button_stackedWidget.widget(i).objectName(): self.Button_stackedWidget.widget(i) 
                          for i in range(self.Button_stackedWidget.count())}

        sorted_pages = sorted(self.manager.config.keys(), 
                             key=lambda x: int(x.split('_')[1]) if '_' in x else 0)

        for page_name in sorted_pages:
            if page_name not in existing_pages:
                page_widget = self.create_page_structure(page_name)
                self.Button_stackedWidget.addWidget(page_widget)
                existing_pages[page_name] = page_widget
            
            page_widget = existing_pages[page_name]
            for btn_name, btn_props in self.manager.config[page_name].items():
                btn = page_widget.findChild(QToolButton, btn_name)
                if btn:
                    self.configure_button(btn, btn_props)

        self.bind_all_buttons()

    def create_page_structure(self, page_name):
        """Создает страницу с сеткой кнопок."""
        page = QWidget()
        page.setObjectName(page_name)
        layout = QGridLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        frame = QFrame(page)
        try:
            page_num = page_name.split('_')[1]
            frame.setObjectName(f"Button_frame_{int(page_num):02d}")
        except:
            frame.setObjectName(f"Button_frame_{page_name}")

        frame_layout = QGridLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(5)
        
        positions = {f"butt_toolB_{i:02d}": ((i-1)//4, (i-1)%4) for i in range(1, 13)}
        
        for btn_name, (r, c) in positions.items():
            btn = QToolButton(frame)
            btn.setObjectName(btn_name)
            btn.setMinimumSize(150, 150)
            btn.setMaximumSize(150, 150)
            btn.setIconSize(QSize(130, 130))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            
            # Настройки, аналогичные статическим кнопкам (Page 1)
            btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            btn.setCheckable(False)
            btn.setAutoRepeatDelay(600)
            btn.setAutoRepeatInterval(300)
            btn.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
            btn.setProperty("applyShadow", True)
            
            frame_layout.addWidget(btn, r, c)
                
        layout.addWidget(frame, 0, 0)
        return page

    def configure_button(self, btn, props):
        """Настройка внешнего вида кнопки."""
        btn.setText("")
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn.setIconSize(QSize(130, 130))
        
        if "icon_path" in props:
            icon_path = os.path.join(self.plugin_path, props["icon_path"])
            if os.path.exists(icon_path):
                icon = QIcon()
                icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                btn.setIcon(icon)

    def bind_all_buttons(self):
        """Подключение сигналов клика."""
        for btn in self.findChildren(QToolButton):
            btn.installEventFilter(self)
            
            # 1. Отключаем только наше предыдущее соединение, если оно существует
            if hasattr(btn, '_click_connection'):
                try:
                    btn.clicked.disconnect(btn._click_connection)
                except (TypeError, RuntimeError):
                    pass
            
            # 2. Создаем новое соединение и сохраняем ссылку на него
            # Используем lambda с захватом текущего btn
            btn._click_connection = btn.clicked.connect(lambda checked=False, b=btn: self.on_ui_button_clicked(b))

    def on_ui_button_clicked(self, btn):
        """Передача клика в менеджер и воспроизведение звука."""
        page_id = "unknown"
        parent = btn.parentWidget()
        while parent and parent != self:
            if "page" in parent.objectName():
                page_id = parent.objectName()
                break
            parent = parent.parentWidget()
            
        # 1. Воспроизведение звука
        btn_name = btn.objectName()
        sound_played = False
        
        # Сначала проверяем глобальный конфиг (context: plugins -> shortcut)
        context_map = self.sound_manager.config_map.get("plugins", {}).get("shortcut", {})
        if btn_name in context_map:
            self.sound_manager.play(context_map[btn_name])
            sound_played = True
        
        # Если в конфиге нет, проверяем свойства самой кнопки (sound_path)
        if not sound_played:
            btn_props = self.manager.get_button_props(btn_name, page_id)
            if btn_props and "sound_path" in btn_props:
                sound_file = os.path.join(self.plugin_path, btn_props["sound_path"])
                if os.path.exists(sound_file):
                    self.sound_manager.play_file(sound_file)
                    sound_played = True
        
        # Звук по умолчанию, если ничего не найдено
        if not sound_played:
            default_sound = os.path.join(self.plugin_path, "resources", "sound", "button_click.wav")
            if os.path.exists(default_sound):
                self.sound_manager.play_file(default_sound)

        # 2. Логика действия
        self.manager.process_button_click(btn.objectName(), page_id)

    def next_page(self):
        idx = self.Button_stackedWidget.currentIndex()
        if idx < self.Button_stackedWidget.count() - 1:
            self.Button_stackedWidget.setCurrentIndex(idx + 1)

    def prev_page(self):
        idx = self.Button_stackedWidget.currentIndex()
        if idx > 0:
            self.Button_stackedWidget.setCurrentIndex(idx - 1)
