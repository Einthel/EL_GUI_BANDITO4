import os
import base64
import json
import requests
import shutil
import subprocess
import shlex
from PySide6.QtWidgets import QWidget, QToolButton, QButtonGroup, QFileDialog, QMenu, QTreeWidgetItem, QAbstractItemView, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QKeySequence, QAction

# Импорт менеджера данных
try:
    from shortcut_save_load import ShortcutDataManager
except ImportError:
    from .shortcut_save_load import ShortcutDataManager

# Импорт диалога сохранения префаба
try:
    from save_prefab_di import SavePrefabDialog
except ImportError:
    from .save_prefab_di import SavePrefabDialog

# Импорт диалога вопросов
try:
    from questions_di import QuestionsDialog
except ImportError:
    from .questions_di import QuestionsDialog

# Импорт диалога выбора приложения
try:
    from app_list_di import AppListDialog
except ImportError:
    from .app_list_di import AppListDialog

# Импорт UI (предполагаем, что он лежит рядом)
try:
    from ui_shortcut_bandito import Ui_stream_bandito
except ImportError:
    from .ui_shortcut_bandito import Ui_stream_bandito

class ShortcutBanditoPlugin(QWidget, Ui_stream_bandito):
    """
    Класс виджета плагина для сервера (интерфейс редактора).
    """
    def __init__(self, plugin_path):
        super().__init__()
        self.plugin_path = plugin_path
        self.setupUi(self)

        # Инициализация текущей страницы
        self.current_page_index = 1
        
        # Переменная для хранения пути к текущей иконке
        self.current_icon_path = None
        
        # Изначально блокируем только редактор
        self.set_editor_enabled(False)
        
        # Загрузка стиля
        self.load_stylesheet()
        
        # Настройка кнопок
        self.setup_buttons()
        
        # Подключение сигналов управления страницами
        self.add_page_toolB.clicked.connect(self.add_page)
        self.remove_page_toolB.clicked.connect(self.remove_page)
        self.next_page_pushB.clicked.connect(self.next_page)
        self.back_page_pushB.clicked.connect(self.prev_page)
        
        # Подключение кнопки выбора иконки
        self.Browse_ico_diy_toolB.clicked.connect(self.browse_icon_handler)
        
        # Подключение кнопки выбора приложения
        self.app_choice_toolB.clicked.connect(self.open_app_selector)
        
        # Подключение сигнала сохранения
        self.save_pushB.clicked.connect(self.save_config) # Оставляем пока как заглушку или удаляем, если кнопка не нужна
        self.save_new_pushB.clicked.connect(self.save_new_shortcut_preset)
        
        # Инициализация менеджера данных
        self.data_manager = ShortcutDataManager(self.plugin_path)
        self.config_data = self.data_manager.get_data()
        
        # Обновляем отображение текущей страницы
        self.refresh_page()
        
        # Загрузка действий в комбобокс
        self.load_actions_config()
        
        # Настройка TreeWidget (Drag & Drop заглушка)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeWidget.setDefaultDropAction(Qt.MoveAction)
        
        # Контекстное меню дерева
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_tree_context_menu)

    def set_editor_enabled(self, enabled):
        """Блокирует/разблокирует элементы редактора кнопок, не трогая навигацию страниц."""
        self.Example_groupB.setEnabled(enabled)
        self.ico_groupB.setEnabled(enabled)
        self.funcrion_widget.setEnabled(enabled)

    def open_app_selector(self):
        """Открывает диалог выбора приложения."""
        dialog = AppListDialog(self)
        if dialog.exec():
            path, name = dialog.get_selected_app()
            if path:
                self.app_path_lineE.setText(path)
                # Если заголовок пустой, заполняем именем приложения
                if not self.app_title_lineE.text():
                    self.app_title_lineE.setText(name)

    def load_stylesheet(self):
        """Загружает стиль из style_shortcut.json."""
        style_path = os.path.join(self.plugin_path, "config", "style_shortcut.json")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)
                    
                # Преобразуем JSON в CSS строку
                css = ""
                for selector, props in style_data.items():
                    props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                    css += f"{selector} {{ {props_str} }} \n"
                
                self.setStyleSheet(css)
                print(f"[ShortcutEditor] Loaded stylesheet from {style_path}")
            except Exception as e:
                print(f"[ShortcutEditor] Error loading stylesheet: {e}")

    def load_actions_config(self):
        """Загружает список доступных действий из config_shortcut.json в комбобокс."""
        config_path = os.path.join(self.plugin_path, "config", "config_shortcut.json")
        if not os.path.exists(config_path):
            return
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.action_comboB.clear()
            actions = data.get("actions", [])
            for action in actions:
                # Добавляем имя действия и сохраняем весь словарь действия как userData
                self.action_comboB.addItem(action.get("name"), action)
                
        except Exception as e:
            print(f"[ShortcutEditor] Error loading actions config: {e}")

    def setup_buttons(self):
        """Группирует кнопки и подключает сигналы."""
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(False) # Отключаем эксклюзивность, чтобы управлять вручную
        
        # Ищем кнопки butt_toolB_01...12
        for i in range(1, 13):
            btn_name = f"butt_toolB_{i:02d}"
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                self.button_group.addButton(btn, i)
                # Подключаем клик напрямую к кнопке для обработки toggling
                # Используем lambda с захватом id
                btn.clicked.connect(lambda checked=False, bid=i: self.on_button_toggled(bid))
                
                # Контекстное меню для удаления
                btn.setContextMenuPolicy(Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(lambda pos, b=btn: self.show_context_menu(pos, b))
                
                # Включаем прием Drop событий
                btn.setAcceptDrops(True)
                # Переопределяем метод dragEnterEvent и dropEvent для конкретной кнопки
                # (делаем это динамически, присваивая метод экземпляру)
                # Но лучше использовать eventFilter или создать подкласс.
                # Т.к. это сгенерированный UI, проще всего использовать eventFilter или патчить методы.
                # Патчинг методов экземпляра:
                btn.dragEnterEvent = lambda e, b=btn: self.btn_dragEnterEvent(e, b)
                btn.dropEvent = lambda e, b=btn: self.btn_dropEvent(e, b)

    def btn_dragEnterEvent(self, event, btn):
        """Обработчик входа перетаскивания на кнопку."""
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()

    def btn_dropEvent(self, event, btn):
        """Обработчик сброса на кнопку."""
        # Получаем данные из дерева
        # QTreeWidget использует application/x-qabstractitemmodeldatalist, но парсить его сложно.
        # Проще получить текущий выбранный элемент в дереве, так как D&D идет оттуда.
        
        selected_items = self.treeWidget.selectedItems()
        if not selected_items: return
        
        item = selected_items[0]
        data = item.data(0, Qt.UserRole)
        if not data: return
        
        prefab_name = data.get("prefab_name")
        if not prefab_name: return
        
        print(f"[ShortcutEditor] Dropped prefab '{prefab_name}' on {btn.objectName()}")
        
        # Загружаем префаб
        prefabs = self.data_manager.get_prefabs()
        if prefab_name in prefabs:
            prefab_data = prefabs[prefab_name]
            
            # Применяем данные к кнопке (сохраняем на страницу)
            # ВАЖНО: Мы копируем данные, но имя берем из префаба (или оставляем как есть?)
            # Обычно берем все из префаба.
            
            # Копируем словарь, чтобы не менять префаб
            new_btn_data = prefab_data.copy()
            
            # Сохраняем
            self.data_manager.update_button(self.current_page_index, btn.objectName(), new_btn_data)
            self.config_data = self.data_manager.get_data()
            
            # Обновляем UI
            self.refresh_page()
            
            # Отправляем обновления (иконку и конфиг)
            icon_path = new_btn_data.get("icon_path")
            if icon_path:
                self.broadcast_icon_update(icon_path)
            self.broadcast_config_update()
            
            event.acceptProposedAction()

    def show_context_menu(self, pos, btn):
        """Отображает контекстное меню для кнопки."""
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        action = menu.exec(btn.mapToGlobal(pos))
        
        if action == delete_action:
            self.delete_button_config(btn)

    def delete_button_config(self, btn):
        """Удаляет конфигурацию кнопки и очищает ее."""
        btn_name = btn.objectName()
        
        # Делегируем удаление менеджеру
        self.data_manager.delete_button(self.current_page_index, btn_name)
        
        # Обновляем локальную ссылку на данные
        self.config_data = self.data_manager.get_data()
            
        # Обновляем отображение страницы (это сбросит кнопку в дефолтное состояние "...")
        self.refresh_page()
        
        # Отправляем обновление
        self.broadcast_config_update()

    def on_button_toggled(self, btn_id):
        """Обработчик переключения кнопки (toggle behavior)."""
        clicked_btn = self.button_group.button(btn_id)
        
        # ВАЖНО: При setExclusive(False) состояние меняется ДО вызова этого сигнала?
        # Или мы должны сами его менять?
        # В QButtonGroup без exclusive состояние кнопки меняется автоматически при клике.
        
        # Если кнопка стала ACTIVE
        if clicked_btn.isChecked():
            # Если мы ВКЛЮЧИЛИ кнопку, выключаем все остальные вручную
            # (так как мы отключили Exclusive)
            for btn in self.button_group.buttons():
                if btn is not clicked_btn:
                    btn.setChecked(False)
            
            # Активируем панель
            self.set_editor_enabled(True)
            
            # Загружаем настройки
            btn_name = clicked_btn.objectName()
            print(f"[ShortcutEditor] Selected button: {btn_name} (ID: {btn_id})")
            self.load_button_settings(btn_name)
            
            # Обновляем пример
            self.update_example_button(btn_name)
            
        # Если кнопка стала INACTIVE
        else:
            # Если мы ВЫКЛЮЧИЛИ кнопку
            print(f"[ShortcutEditor] Deselected button (ID: {btn_id})")
            
            # Деактивируем панель
            self.set_editor_enabled(False)
            
            self.clear_editor_fields()
            
            # Сбрасываем пример
            self.Example_toolB.setText("...")
            self.Example_toolB.setIcon(QIcon())

    # --- Методы управления страницами ---
    def add_page(self):
        """Добавляет новую страницу."""
        # Делегируем создание страницы менеджеру
        new_index = self.data_manager.add_new_page()
        print(f"[ShortcutEditor] Added new page: page_{new_index}")
        
        # Обновляем данные и переключаемся
        self.config_data = self.data_manager.get_data()
        self.current_page_index = new_index
        self.refresh_page()
        
        # Отправляем обновление
        self.broadcast_config_update()

    def remove_page(self):
        """Удаляет текущую страницу."""
        # Делегируем удаление менеджеру
        # Он вернет нам корректный индекс страницы, на которую нужно переключиться
        new_current_index = self.data_manager.remove_page(self.current_page_index)
        
        self.config_data = self.data_manager.get_data()
        self.current_page_index = new_current_index
        self.refresh_page()
        
        # Отправляем обновление
        self.broadcast_config_update()

    def next_page(self):
        """Переключает на следующую страницу."""
        # Проверяем, существует ли следующая страница
        next_page_key = f"page_{self.current_page_index + 1}"
        
        # Простая проверка по ключу в конфиге
        if next_page_key in self.config_data:
            self.current_page_index += 1
            print(f"[ShortcutEditor] Switched to page {self.current_page_index}")
            self.refresh_page()
        else:
            print("[ShortcutEditor] No next page available")

    def prev_page(self):
        """Переключает на предыдущую страницу."""
        if self.current_page_index > 1:
            self.current_page_index -= 1
            print(f"[ShortcutEditor] Switched to page {self.current_page_index}")
            self.refresh_page()

    def save_config(self):
        """
        Принудительное сохранение конфигурации и отправка клиентам.
        """
        self.data_manager.save()
        print(f"[ShortcutEditor] Config saved via explicit call")
        
        # Отправляем обновление клиентам
        self.broadcast_config_update()

    def broadcast_config_update(self):
        """Отправляет обновленный конфиг всем подключенным клиентам."""
        try:
            # Читаем актуальные данные
            config_data = self.data_manager.get_data()
            
            # Формируем сообщение
            payload = {
                "command": "SHORTCUT_CONFIG_UPDATE",
                "data": config_data
            }
            
            # Определяем порт из конфига (нужно бы его передавать, но пока хардкод 8000 или чтение)
            # Для надежности попробуем прочитать конфиг сервера, если он доступен, или использовать дефолт
            port = 8000 
            # (В идеале plugin_path -> ... -> configs/el_bandito_config.json, но для скорости пока так)
            
            url = f"http://127.0.0.1:{port}/api/broadcast"
            
            # Отправляем POST запрос локальному серверу
            response = requests.post(url, json=payload, timeout=0.5)
            
            if response.status_code == 200:
                print("[ShortcutEditor] Config update broadcasted successfully")
            else:
                print(f"[ShortcutEditor] Broadcast failed: {response.status_code}")
                
        except Exception as e:
            print(f"[ShortcutEditor] Error broadcasting config: {e}")

    def broadcast_icon_update(self, icon_rel_path):
        """
        Отправляет файл иконки клиентам.
        icon_rel_path: относительный путь (plugins/shortcut/resources/ico/name.png)
        """
        if not icon_rel_path:
            return

        full_path = os.path.join(self.plugin_path, icon_rel_path)
        # Если путь уже абсолютный или начинается с resources внутри плагина
        if not os.path.exists(full_path):
             # Попробуем считать, что icon_rel_path это путь от корня плагина
             # но у нас self.plugin_path это корень плагина.
             # А в конфиге путь записан как 'resources/ico/...' или 'plugins/shortcut/resources/ico/...'
             # Надо быть аккуратным.
             
             # Вариант А: путь 'resources/ico/x.png' -> self.plugin_path/resources/ico/x.png
             if os.path.exists(os.path.join(self.plugin_path, icon_rel_path)):
                 full_path = os.path.join(self.plugin_path, icon_rel_path)
             # Вариант Б: путь 'plugins/shortcut/resources/ico/x.png' (полный относительный от корня проекта)
             # Тогда нам надо подняться на 2 уровня вверх от self.plugin_path? 
             # Нет, проще проверить существование.
             elif os.path.exists(icon_rel_path):
                 full_path = icon_rel_path
             else:
                 print(f"[ShortcutEditor] Icon file not found for broadcast: {full_path}")
                 return

        try:
            with open(full_path, "rb") as f:
                file_content = f.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
            
            # Формируем сообщение.
            # Важно: клиенту нужен путь относительно корня плагина или проекта?
            # В конфиге путь лежит как 'resources/ico/...' (обычно)
            # Или 'plugins/shortcut/resources/ico/...'?
            # В save_new_shortcut_preset мы сохраняем:
            # icon_path_to_save = self.current_icon_path if self.current_icon_path else "resources/ico/ico_shortcut.png"
            # Значит путь относительный от корня плагина (если мы в папке плагина) ИЛИ от корня проекта.
            # Посмотрим browse_icon_handler:
            # rel_path = f"resources/ico/{file_name}"
            # Значит это путь ОТНОСИТЕЛЬНО ПАПКИ ПЛАГИНА (или рабочей директории, если она совпадает).
            
            # Но клиентский апдейтер кладет файлы в ROOT_DIR/plugins/shortcut/resources/ico
            # Значит клиенту мы должны сказать, куда положить файл.
            
            # Отправляем относительный путь от корня плагина
            payload = {
                "command": "SHORTCUT_ICON_UPDATE",
                "data": {
                    "path": icon_rel_path,
                    "content": encoded_content
                }
            }
            
            port = 8000
            url = f"http://127.0.0.1:{port}/api/broadcast"
            requests.post(url, json=payload, timeout=0.5)
            print(f"[ShortcutEditor] Icon broadcasted: {icon_rel_path}")
            
        except Exception as e:
            print(f"[ShortcutEditor] Error broadcasting icon: {e}")

    def save_new_shortcut_preset(self):
        """Сохраняет новую кнопку (пресет) типа 'shortcut' или 'system'."""
        print("[ShortcutEditor] Save new preset clicked")
        
        # 1. Находим активную кнопку (через цикл, т.к. exclusive=False)
        checked_btn = None
        for btn in self.button_group.buttons():
            if btn.isChecked():
                checked_btn = btn
                break
        
        if not checked_btn:
            print("[ShortcutEditor] No button selected")
            return
            
        btn_name = checked_btn.objectName()
        
        # 2. Определяем активную вкладку и собираем данные
        current_tab_index = self.funcrion_widget.currentIndex()
        
        name = "New Button"
        action_type = "shortcut"
        action_value = ""
        
        # Вкладка Application (Index 0) - NEW
        if current_tab_index == 0:
            name = self.app_title_lineE.text()
            if not name: name = "New App"
            
            action_value = self.app_path_lineE.text()
            action_type = "program"
            
            if not action_value:
                print("[ShortcutEditor] Warning: No application path selected")
                # Можно вернуть return, но позволим сохранить пустышку
        
        # Вкладка Shortcuts (Index 1)
        elif current_tab_index == 1:
            name = self.sh_title_lineE.text()
            if not name: name = "New Shortcut"
            
            key_seq = self.sh_hc1_keyEdit.keySequence()
            action_value = key_seq.toString(QKeySequence.SequenceFormat.NativeText)
            action_type = "shortcut"
            
        # Вкладка Action (Index 2)
        elif current_tab_index == 2:
            name = self.action_title_lineE.text()
            if not name: name = "New Action"
            
            # Получаем данные из комбобокса
            current_idx = self.action_comboB.currentIndex()
            if current_idx >= 0:
                # Получаем userData, который содержит весь словарь действия
                selected_action_data = self.action_comboB.itemData(current_idx)
                
                if isinstance(selected_action_data, dict):
                    action_type = selected_action_data.get("type", "system")
                    action_value = selected_action_data.get("value", "")
                else:
                    print(f"[ShortcutEditor] Warning: Invalid item data at index {current_idx}: {selected_action_data}")
                    return
            else:
                print("[ShortcutEditor] No action selected in combobox")
                return
        
        else:
             print(f"[ShortcutEditor] Current tab {current_tab_index} not supported for saving yet.")
             return

        # 3. Формируем структуру данных
        # Используем сохраненный путь или дефолт
        icon_path_to_save = self.current_icon_path if self.current_icon_path else "resources/ico/ico_shortcut.png"
        
        new_btn_data = {
            "name": name,
            "icon_path": icon_path_to_save,
            "icon_size": 70,
            "action": {
                "type": action_type,
                "value": action_value
            }
        }
        
        # --- NEW: Открываем диалог сохранения префаба с проверкой дубликатов ---
        existing_prefabs = self.data_manager.get_prefabs()
        current_name_to_edit = name # Имя для предзаполнения
        
        while True:
            dialog = SavePrefabDialog(self, default_name=current_name_to_edit)
            if dialog.exec() == QDialog.Accepted:
                prefab_name = dialog.get_prefab_name()
                if not prefab_name: continue # Если пустое (хотя кнопка должна быть заблокирована)
                
                # Проверка на дубликаты
                if prefab_name in existing_prefabs:
                    q_text = f"Prefab '{prefab_name}' already exists.\nOverwrite?"
                    q_dialog = QuestionsDialog(self, question_text=q_text)
                    if q_dialog.exec() == QDialog.Accepted:
                        # Пользователь согласился перезаписать
                        self.data_manager.save_prefab(prefab_name, new_btn_data)
                        print(f"[ShortcutEditor] Overwrote prefab: {prefab_name}")
                        break # Выходим из цикла
                    else:
                        # Пользователь отказался, возвращаемся к вводу имени
                        current_name_to_edit = prefab_name # Оставляем то, что он ввел
                        continue # Перезапускаем цикл
                else:
                    # Имя уникальное, сохраняем
                    self.data_manager.save_prefab(prefab_name, new_btn_data)
                    print(f"[ShortcutEditor] Saved new prefab: {prefab_name}")
                    break # Выходим из цикла
            else:
                print("[ShortcutEditor] Prefab saving cancelled by user")
                return # Отмена всего действия

        # 4. Делегируем сохранение менеджеру (на страницу)
        self.data_manager.update_button(self.current_page_index, btn_name, new_btn_data)
        
        # 5. Обновляем локальные данные
        self.config_data = self.data_manager.get_data()
        
        # 6. Обновляем UI (кнопку в сетке)
        checked_btn.setText(name)
        
        # Грузим иконку
        icon_path_full = os.path.join(self.plugin_path, icon_path_to_save)
        if os.path.exists(icon_path_full):
            checked_btn.setIcon(QIcon(icon_path_full))
            checked_btn.setIconSize(api_qt_size(70, 70))
        else:
             print(f"[ShortcutEditor] Icon not found: {icon_path_full}")
            
        # Обновляем пример
        self.update_example_button(btn_name)
        
        # 7. Отправляем обновление клиентам
        # Сначала иконку (чтобы она уже была когда придет конфиг)
        self.broadcast_icon_update(icon_path_to_save)
        # Затем конфиг
        self.broadcast_config_update()
        
        # Обновляем дерево (так как добавился префаб)
        self.update_tree_view()
        
        print(f"[ShortcutEditor] Saved preset for {btn_name}: {name} -> {action_value}")

    def clear_editor_fields(self):
        """Очищает поля редактора."""
        self.sh_title_lineE.clear()
        # Тут можно очистить остальные поля

    # def load_config(self): Удален, используется менеджер

    def refresh_page(self):
        """Обновляет кнопки на основе текущей страницы."""
        # Обновляем метку страницы
        if hasattr(self, 'current_page_lable'):
             self.current_page_lable.setText(f"Page {self.current_page_index}")
        
        # Получаем данные текущей страницы
        page_key = f"page_{self.current_page_index}"
        page_data = self.config_data.get(page_key, {})
        
        # Сначала блокируем сигналы у группы кнопок, чтобы не вызвать on_button_toggled
        # Но QButtonGroup не имеет метода blockSignals для своих кнопок скопом.
        # Поэтому проходим по кнопкам.
        
        for i in range(1, 13):
            btn_name = f"butt_toolB_{i:02d}"
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                
                # Временно блокируем сигналы
                btn.blockSignals(True)
                
                # Сбрасываем выделение (мы обновляем всю страницу)
                btn.setChecked(False)
                
                if btn_name in page_data:
                    props = page_data[btn_name]
                    name = props.get("name", "...")
                    btn.setText(name)
                    
                    # Иконка
                    icon_path_rel = props.get("icon_path")
                    if icon_path_rel:
                        icon_full_path = os.path.join(self.plugin_path, icon_path_rel)
                        if os.path.exists(icon_full_path):
                            # Грузим иконку
                            btn.setIcon(QIcon(icon_full_path))
                            # Размер
                            size = props.get("icon_size", 64)
                            btn.setIconSize(api_qt_size(size, size))
                        else:
                            btn.setIcon(QIcon())
                    else:
                        btn.setIcon(QIcon())
                else:
                    # Пустая кнопка
                    btn.setText("...")
                    btn.setIcon(QIcon())
                
                btn.blockSignals(False)

        # Сбрасываем панель настроек
        self.set_editor_enabled(False)
        self.clear_editor_fields()
        
        # Сбрасываем пример
        self.Example_toolB.setText("...")
        self.Example_toolB.setIcon(QIcon())
        
        # Управление кнопками навигации
        self.back_page_pushB.setEnabled(self.current_page_index > 1)
        
        # Проверяем наличие следующей страницы для активации кнопки Next
        next_page_key = f"page_{self.current_page_index + 1}"
        self.next_page_pushB.setEnabled(next_page_key in self.config_data)
        
        # Обновляем дерево кнопок
        self.update_tree_view()

    def show_tree_context_menu(self, pos):
        """Отображает контекстное меню для дерева префабов."""
        item = self.treeWidget.itemAt(pos)
        if not item: return
        
        # Если есть родитель, значит это префаб (а не категория)
        if item.parent():
            menu = QMenu(self.treeWidget)
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            
            action = menu.exec(self.treeWidget.mapToGlobal(pos))
            
            if action == delete_action:
                self.delete_prefab_handler(item)
            elif action == rename_action:
                self.rename_prefab_handler(item)

    def delete_prefab_handler(self, item):
        """Удаляет выбранный префаб."""
        data = item.data(0, Qt.UserRole)
        prefab_name = data.get("prefab_name")
        if not prefab_name: return
        
        q_text = f"Delete prefab '{prefab_name}'?"
        dialog = QuestionsDialog(self, question_text=q_text)
        if dialog.exec() == QDialog.Accepted:
            self.data_manager.delete_prefab(prefab_name)
            self.update_tree_view()

    def rename_prefab_handler(self, item):
        """Переименовывает префаб."""
        data = item.data(0, Qt.UserRole)
        current_name = data.get("prefab_name")
        if not current_name: return
        
        existing_prefabs = self.data_manager.get_prefabs()
        
        dialog = SavePrefabDialog(self, default_name=current_name)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.get_prefab_name()
            
            if new_name == current_name: return
            
            if new_name in existing_prefabs:
                # Если имя занято (и это не мы сами)
                q_text = f"Name '{new_name}' already exists.\nOverwrite?"
                q_dialog = QuestionsDialog(self, question_text=q_text)
                if q_dialog.exec() == QDialog.Accepted:
                    # Перезапись (удаляем старый с таким именем, переименовываем текущий)
                    # Но метод rename_prefab просто перезапишет по ключу.
                    self.data_manager.rename_prefab(current_name, new_name)
                    self.update_tree_view()
                # Если Cancel - ничего не делаем
            else:
                self.data_manager.rename_prefab(current_name, new_name)
                self.update_tree_view()

    def update_tree_view(self):
        """Обновляет дерево кнопок (TreeWidget) данными из ПРЕФАБОВ."""
        self.treeWidget.clear()
        
        # Создаем категории
        cat_app = QTreeWidgetItem(self.treeWidget, ["Application"])
        cat_shortcut = QTreeWidgetItem(self.treeWidget, ["Shortcut"])
        cat_action = QTreeWidgetItem(self.treeWidget, ["Action"])
        cat_other = QTreeWidgetItem(self.treeWidget, ["Other"])
        
        # Разворачиваем категории
        cat_app.setExpanded(True)
        cat_shortcut.setExpanded(True)
        cat_action.setExpanded(True)
        
        # Получаем список префабов
        prefabs = self.data_manager.get_prefabs()
        
        for prefab_name, prefab_data in prefabs.items():
            # prefab_name - это уникальный ID/Имя префаба (например "My Copy Button")
            # prefab_data["name"] - это текст на кнопке (например "Copy")
            
            display_text = f"{prefab_name} ({prefab_data.get('name', '')})"
            
            action = prefab_data.get("action", {})
            act_type = action.get("type", "unknown")
            
            # Создаем элемент дерева
            item = QTreeWidgetItem([prefab_name]) # Используем имя префаба как основной текст
            item.setToolTip(0, f"Button Text: {prefab_data.get('name')}")
            
            # Добавляем иконку
            icon_path_rel = prefab_data.get("icon_path")
            if icon_path_rel:
                icon_full_path = os.path.join(self.plugin_path, icon_path_rel)
                if os.path.exists(icon_full_path):
                    item.setIcon(0, QIcon(icon_full_path))
            
            # Сохраняем метаданные для D&D
            # В data(UserRole) теперь храним имя префаба
            item.setData(0, Qt.UserRole, {"prefab_name": prefab_name})
            
            # Распределяем по категориям
            if act_type == "program":
                cat_app.addChild(item)
            elif act_type == "shortcut":
                cat_shortcut.addChild(item)
            elif act_type == "system" or act_type == "action":
                cat_action.addChild(item)
            else:
                cat_other.addChild(item)

    def update_example_button(self, btn_name):
        """Обновляет Example_toolB данными выбранной кнопки."""
        if not hasattr(self, 'config_data'): return
        
        # Получаем данные текущей страницы
        page_key = f"page_{self.current_page_index}"
        page_data = self.config_data.get(page_key, {})
        btn_data = page_data.get(btn_name, {})
        
        # Текст
        name = btn_data.get("name", "...")
        self.Example_toolB.setText(name)
        
        # Иконка
        icon_path_rel = btn_data.get("icon_path")
        if icon_path_rel:
            icon_full_path = os.path.join(self.plugin_path, icon_path_rel)
            if os.path.exists(icon_full_path):
                self.Example_toolB.setIcon(QIcon(icon_full_path))
                
                # Размер иконки
                size = btn_data.get("icon_size", 64)
                self.Example_toolB.setIconSize(api_qt_size(size, size))
        else:
            self.Example_toolB.setIcon(QIcon())

    def on_button_clicked(self, btn_id):
        # Этот метод больше не используется напрямую, логика перенесена в on_button_toggled
        pass

    def browse_icon_handler(self):
        """Обработчик нажатия кнопки выбора иконки."""
        print("[ShortcutEditor] Browse icon clicked")
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            "",
            "Images (*.png *.xpm *.jpg *.ico *.svg);;All Files (*)"
        )
        
        if not file_path:
            return
            
        print(f"[ShortcutEditor] Selected file: {file_path}")
        
        # Определяем папку назначения
        ico_dir = os.path.join(self.plugin_path, "resources", "ico")
        if not os.path.exists(ico_dir):
            os.makedirs(ico_dir)
            
        # Копируем файл
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(ico_dir, file_name)
        
        try:
            # Проверяем, не выбираем ли мы файл, который уже лежит в целевой папке
            if os.path.abspath(file_path) != os.path.abspath(dest_path):
                 shutil.copy2(file_path, dest_path)
                 print(f"[ShortcutEditor] Copied icon to: {dest_path}")
            else:
                 print(f"[ShortcutEditor] File is already in destination, skipping copy: {dest_path}")
            
            # Сохраняем относительный путь
            rel_path = f"resources/ico/{file_name}"
            self.current_icon_path = rel_path
            
            # Обновляем превью
            self.Example_toolB.setIcon(QIcon(dest_path))
            self.Example_toolB.setIconSize(api_qt_size(70, 70))
            
        except Exception as e:
            print(f"[ShortcutEditor] Error copying icon: {e}")

    def load_button_settings(self, btn_name):
        """Заполняет поля справа данными выбранной кнопки."""
        # Очистка полей
        self.clear_editor_fields()
        
        if not hasattr(self, 'config_data'):
            return

        # Получаем данные текущей страницы
        page_key = f"page_{self.current_page_index}"
        page_data = self.config_data.get(page_key, {})
        btn_data = page_data.get(btn_name, {})
        
        # Загружаем путь к иконке
        icon_path = btn_data.get("icon_path", "")
        if icon_path:
            self.current_icon_path = icon_path
        else:
            self.current_icon_path = None
        
        # Заполнение Title
        name = btn_data.get("name", "")
        
        # Блокируем сигналы, чтобы не триггерить on_name_changed
        self.app_title_lineE.blockSignals(True)
        self.sh_title_lineE.blockSignals(True)
        self.action_title_lineE.blockSignals(True)
        
        self.app_title_lineE.setText(name)
        self.sh_title_lineE.setText(name)
        self.action_title_lineE.setText(name)
        
        self.app_title_lineE.blockSignals(False)
        self.sh_title_lineE.blockSignals(False)
        self.action_title_lineE.blockSignals(False)
            
        # Заполнение Action
        action = btn_data.get("action", {})
        act_type = action.get("type")
        act_value = action.get("value")
        
        # Заполнение для Program (Tab 0)
        if act_type == "program":
            self.app_path_lineE.setText(act_value)
        else:
            self.app_path_lineE.clear()
        
        if act_type == "shortcut" and act_value:
            self.sh_hc1_keyEdit.setKeySequence(QKeySequence(act_value))
        else:
            self.sh_hc1_keyEdit.clear()
            
        # Заполнение Action из Combo (Tab 2)
        if act_type == "system":
            # Ищем индекс элемента с нужным значением
            index = -1
            for i in range(self.action_comboB.count()):
                data = self.action_comboB.itemData(i)
                if data and data.get("value") == act_value:
                    index = i
                    break
            if index != -1:
                self.action_comboB.setCurrentIndex(index)

def api_qt_size(w, h):
    from PySide6.QtCore import QSize
    return QSize(w, h)

# --- Функции для обработки команд от клиента (остаются глобальными или статическими) ---

def handle_button_press(btn_id_full, plugin_path):
    """
    Обрабатывает нажатие кнопки (вызывается из el_bandito.py).
    """
    print(f"[ShortcutServer] Handling button press: {btn_id_full}")
    
    # ... (код парсинга и выполнения действия) ...
    # Дублируем логику execute_action сюда или выносим в утилиты
    # Для простоты пока оставим здесь, но в идеале нужно рефакторить
    
    try:
        page_num, btn_name = btn_id_full.split(":")
    except ValueError:
        return

    config_path = os.path.join(plugin_path, "config", "button_shortcut.json")
    if not os.path.exists(config_path):
        return
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception:
        return

    page_key = f"page_{page_num}"
    page_data = config.get(page_key, {})
    btn_data = page_data.get(btn_name, {})
    action = btn_data.get("action")
    
    if action:
        execute_action(action)

def execute_action(action):
    # ... (существующая функция execute_action) ...
    act_type = action.get("type")
    value = action.get("value")
    
    print(f"[ShortcutServer] Executing: {act_type} -> {value}")
    
    if act_type == "program":
        try:
            subprocess.Popen(value, shell=True)
        except Exception as e:
             print(f"[ShortcutServer] Error: {e}")
             
    elif act_type == "shortcut":
        try:
            import keyboard
            hotkey_str = value.lower().replace("win", "windows")
            keyboard.send(hotkey_str)
        except Exception as e:
            print(f"[ShortcutServer] Error: {e}")

