import base64
import os
import json
from PySide6.QtWidgets import QWidget, QToolButton, QGridLayout, QFrame
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

# Импортируем сгенерированный UI файл
# Важно: имя модуля зависит от того, как он называется в папке.
# В данном случае предполагается, что он лежит рядом.
from ui_shortcut_cliento import Ui_stream_cliento

class ShortcutClientPlugin(QWidget, Ui_stream_cliento):
    def __init__(self, socket_client, plugin_path):
        super().__init__()
        self.socket_client = socket_client
        self.plugin_path = plugin_path
        
        # Инициализация UI
        self.setupUi(self)
        
        # Загрузка конфигурации внешнего вида кнопок
        self.config = self.load_config()
        
        # Настройка кнопок
        self.setup_buttons()
        
        # Подписываемся на сообщения от сервера
        if self.socket_client:
            self.socket_client.message_received.connect(self.on_server_message)
            print("[ShortcutPlugin] Subscribed to socket messages")

    def on_server_message(self, data):
        """Обработка сообщений от сервера, специфичных для этого плагина."""
        command = data.get("command")
        
        if command == "SHORTCUT_CONFIG_UPDATE":
            new_config = data.get("data")
            if new_config:
                print("[ShortcutPlugin] Received config update from server")
                self.handle_config_update(new_config)
                
        elif command == "SHORTCUT_ICON_UPDATE":
            icon_data = data.get("data")
            if icon_data:
                print("[ShortcutPlugin] Received icon update from server")
                self.handle_icon_update(icon_data)

    def handle_icon_update(self, icon_data):
        """Сохраняет новую иконку на диск."""
        rel_path = icon_data.get("path")
        content_b64 = icon_data.get("content")
        
        if not rel_path or not content_b64:
            return
            
        # Формируем полный путь
        # rel_path приходит как 'resources/ico/name.png'
        # self.plugin_path указывает на корень плагина
        full_path = os.path.join(self.plugin_path, rel_path)
        
        try:
            # Создаем папку, если нет
            dir_path = os.path.dirname(full_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                
            # Декодируем и пишем
            file_data = base64.b64decode(content_b64)
            with open(full_path, "wb") as f:
                f.write(file_data)
                
            print(f"[ShortcutPlugin] Icon saved: {full_path}")
            
        except Exception as e:
            print(f"[ShortcutPlugin] Error saving icon: {e}")

    def handle_config_update(self, new_config):
        """Применяет новую конфигурацию и сохраняет её."""
        # 1. Сохраняем в память
        self.config = new_config
        
        # 2. Сохраняем в файл (чтобы при рестарте было актуально)
        config_path = os.path.join(self.plugin_path, "config", "button_shortcut.json")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            print(f"[ShortcutPlugin] Config updated and saved to disk")
        except Exception as e:
            print(f"[ShortcutPlugin] Error saving updated config: {e}")
            
        # 3. Перестраиваем UI
        # Для безопасности (вдруг мы не в главном потоке?) - но сигналы Qt обычно безопасны
        # Сначала очищаем старые кнопки
        self.clear_ui()
        # Затем строим заново
        self.setup_buttons()

    def clear_ui(self):
        """Очищает страницы кнопок перед обновлением."""
        # Удаляем все страницы из StackedWidget
        while self.Button_stackedWidget.count() > 0:
            widget = self.Button_stackedWidget.widget(0)
            self.Button_stackedWidget.removeWidget(widget)
            widget.deleteLater()

    def load_config(self):
        """Загружает конфигурацию кнопок из JSON."""
        config_path = os.path.join(self.plugin_path, "config", "button_shortcut.json")
        print(f"[ShortcutPlugin] Loading config from: {config_path}")
        
        if not os.path.exists(config_path):
            print(f"[ShortcutPlugin] Config not found: {config_path}")
            return {}
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"[ShortcutPlugin] Config loaded successfully. Pages found: {list(data.keys())}")
                return data
        except Exception as e:
            print(f"[ShortcutPlugin] Error loading config: {e}")
            return {}

    def setup_buttons(self):
        """Находит кнопки в UI, настраивает их вид и подключает сигналы."""
        print("[ShortcutPlugin] Setting up buttons...")
        buttons_configured = 0
        
        # Получаем список существующих страниц в StackedWidget
        existing_pages = {}
        for i in range(self.Button_stackedWidget.count()):
            widget = self.Button_stackedWidget.widget(i)
            existing_pages[widget.objectName()] = widget

        # Проходим по страницам из конфига
        # Сортируем ключи, чтобы страницы создавались по порядку (page_1, page_2...)
        sorted_pages = sorted(self.config.keys(), key=lambda x: int(x.split('_')[1]) if '_' in x else 0)

        for page_name in sorted_pages:
            buttons_data = self.config[page_name]
            
            # Если страницы нет, создаем её
            if page_name not in existing_pages:
                page_widget = self.create_page_structure(page_name)
                self.Button_stackedWidget.addWidget(page_widget)
                existing_pages[page_name] = page_widget
                print(f"[ShortcutPlugin] Created new page: {page_name}")
            
            page_widget = existing_pages[page_name]
            
            # Ищем кнопки на этой странице
            # Важно: кнопки ищем внутри виджета страницы, а не через self
            for btn_name, btn_props in buttons_data.items():
                btn = page_widget.findChild(QToolButton, btn_name)
                if btn:
                    self.configure_button(btn, btn_props)
                    buttons_configured += 1
                else:
                    # Если кнопки нет (например, на новой странице), создаем заглушки или игнорируем?
                    # В create_page_structure мы должны были создать все 12 кнопок.
                    print(f"[ShortcutPlugin] Warning: Button '{btn_name}' not found on {page_name}.")
        
        print(f"[ShortcutPlugin] Configured {buttons_configured} buttons from config.")

        # АВТО-БИНДИНГ:
        self.bind_all_buttons()

    def create_page_structure(self, page_name):
        """Создает структуру страницы с 12 кнопками, аналогичную page_1."""
        page = QWidget()
        page.setObjectName(page_name)
        
        # Основной layout страницы
        layout = QGridLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Фрейм для кнопок (для стиля)
        frame = QFrame(page)
        frame.setFrameShape(QFrame.Shape.NoFrame)
        frame.setFrameShadow(QFrame.Shadow.Plain)
        
        frame_layout = QGridLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(5)
        
        # Создаем 12 кнопок
        # Схема расположения (как в UI файле):
        # 01 (0,0) | 02 (0,1) | 03 (0,2) | 04 (0,3)
        # 05 (1,0) | 06 (1,1) | 07 (1,2) | 08 (1,3)
        # 09 (2,0) | 10 (2,1) | 11 (2,2) | 12 (2,3)
        
        positions = {
            "butt_toolB_01": (0, 0), "butt_toolB_02": (0, 1), "butt_toolB_03": (0, 2), "butt_toolB_04": (0, 3),
            "butt_toolB_05": (1, 0), "butt_toolB_06": (1, 1), "butt_toolB_07": (1, 2), "butt_toolB_08": (1, 3),
            "butt_toolB_09": (2, 0), "butt_toolB_10": (2, 1), "butt_toolB_11": (2, 2), "butt_toolB_12": (2, 3)
        }
        
        for i in range(1, 13):
            btn_name = f"butt_toolB_{i:02d}"
            btn = QToolButton(frame)
            btn.setObjectName(btn_name)
            btn.setMinimumSize(150, 150)
            btn.setIconSize(api_qt_size(70, 70))
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setText("...")
            
            # Добавляем в layout
            if btn_name in positions:
                r, c = positions[btn_name]
                frame_layout.addWidget(btn, r, c)
                
        layout.addWidget(frame, 0, 0)
        return page

    def configure_button(self, btn, props):
        """Применяет настройки вида к кнопке."""
        if "name" in props:
            btn.setText(props["name"])
        
        if "icon_path" in props:
            # Путь к иконке может быть относительным
            icon_full_path = os.path.join(self.plugin_path, props["icon_path"])
            if os.path.exists(icon_full_path):
                icon = QIcon()
                icon.addPixmap(QPixmap(icon_full_path), QIcon.Normal, QIcon.Off)
                btn.setIcon(icon)
                
                if "icon_size" in props:
                    size = props["icon_size"]
                    btn.setIconSize(api_qt_size(size, size)) # Нужно импортировать QSize если использовать

    def bind_all_buttons(self):
        """Подключает сигнал clicked ко всем QToolButton в плагине."""
        # findChildren находит все дочерние виджеты рекурсивно
        all_buttons = self.findChildren(QToolButton)
        print(f"[ShortcutPlugin] Found {len(all_buttons)} total buttons in UI. Binding signals...")
        
        for btn in all_buttons:
            # Используем lambda с захватом переменной btn
            btn.clicked.connect(lambda checked=False, b=btn: self.on_button_clicked(b))

    def on_button_clicked(self, btn):
        """Обработчик нажатия любой кнопки."""
        btn_id = btn.objectName()
        print(f"[ShortcutPlugin] CLICK DETECTED on button: {btn_id}")
        
        # Определяем страницу (родителя)
        page_id = "unknown"
        parent = btn.parentWidget()
        while parent and parent != self:
            if "page" in parent.objectName():
                page_id = parent.objectName()
                break
            parent = parent.parentWidget()
            
        page_num = page_id.replace("page_", "") if "page_" in page_id else "1"
        
        # 1. Проверяем локальные действия (например, переключение страниц)
        if page_id in self.config and btn_id in self.config[page_id]:
            action = self.config[page_id][btn_id].get("action", {})
            act_type = action.get("type")
            act_value = action.get("value")
            
            if act_type == "system":
                print(f"[ShortcutPlugin] Executing local system action: {act_value}")
                if act_value == "page_prev":
                    self.prev_page()
                    return # Локальное действие выполнено, не отправляем на сервер
                elif act_value == "page_next":
                    self.next_page()
                    return # Локальное действие выполнено, не отправляем на сервер

        # 2. Если не локальное действие, отправляем на сервер
        payload_str = f"{page_num}:{btn_id}"
        print(f"[ShortcutPlugin] Sending payload to server: {payload_str}")
        
        if self.socket_client:
            self.socket_client.send_command("PLUGIN_BUTTON_PRESS", {"id": payload_str})
        else:
            print("[ShortcutPlugin] Error: No socket client connected!")

    def next_page(self):
        """Переключает на следующую страницу."""
        current_idx = self.Button_stackedWidget.currentIndex()
        if current_idx < self.Button_stackedWidget.count() - 1:
            self.Button_stackedWidget.setCurrentIndex(current_idx + 1)
        else:
            # Циклическое переключение? Или стоп? Пока стоп.
            pass

    def prev_page(self):
        """Переключает на предыдущую страницу."""
        current_idx = self.Button_stackedWidget.currentIndex()
        if current_idx > 0:
            self.Button_stackedWidget.setCurrentIndex(current_idx - 1)

def api_qt_size(w, h):
    from PySide6.QtCore import QSize
    return QSize(w, h)
