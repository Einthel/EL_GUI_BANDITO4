import os
import json
from PySide6.QtWidgets import QWidget, QButtonGroup, QFileDialog, QMenu, QTreeWidgetItem, QAbstractItemView, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence

# Импорты менеджера и сервиса
try:
    from .src.sh_bandito_manager import ShortcutBanditoManager
    from .src.sh_bandito_service import (
        load_json, parse_style_to_css, copy_icon_to_plugin
    )
except ImportError:
    from src.sh_bandito_manager import ShortcutBanditoManager
    from src.sh_bandito_service import (
        load_json, parse_style_to_css, copy_icon_to_plugin
    )

# Импорты диалогов
try:
    from src.save_prefab_di import SavePrefabDialog
    from src.questions_di import QuestionsDialog
    from src.app_list_di import AppListDialog
    from src.ico_list_di import IcoListDialog
except ImportError:
    from .src.save_prefab_di import SavePrefabDialog
    from .src.questions_di import QuestionsDialog
    from .src.app_list_di import AppListDialog
    from .src.ico_list_di import IcoListDialog

# Импорт UI
try:
    ui_path = os.path.join(os.path.dirname(__file__), "resources", "ui_done", "ui_shortcut_bandito.py")
    if os.path.exists(ui_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("ui_shortcut_bandito_mod", ui_path)
        ui_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ui_mod)
        Ui_stream_bandito = ui_mod.Ui_stream_bandito
    else:
        from resources.ui_done.ui_shortcut_bandito import Ui_stream_bandito
except Exception as e:
    print(f"[ShortcutBandito] Error loading UI: {e}")
    Ui_stream_bandito = object

class ShortcutBanditoPlugin(QWidget, Ui_stream_bandito):
    def __init__(self, plugin_path, core=None):
        super().__init__()
        self.plugin_path = plugin_path
        self.core = core
        self.setupUi(self)

        # Инициализация менеджера
        self.manager = ShortcutBanditoManager(self.plugin_path, core=core)
        self.manager.config_updated.connect(self.refresh_page)
        
        # Переменные состояния UI
        self.current_icon_path = None
        self.set_editor_enabled(False)
        
        # Инициализация звука
        from el_core.el_sound_manager import ElSoundManager
        self.sound_manager = ElSoundManager(self)
        sound_cfg_path = os.path.join(os.path.dirname(os.path.dirname(self.plugin_path)), "configs", "el_sound_config.json")
        self.sound_manager.load_config(sound_cfg_path)
        
        # Настройка UI
        self.load_stylesheet()
        self.setup_buttons()
        self.setup_connections()
        self.load_actions_config()
        
        # Обновление отображения
        self.refresh_page()
        
        # Настройка TreeWidget
        self.setup_tree_widget()

    def setup_connections(self):
        """Подключение сигналов UI."""
        self.add_page_toolB.clicked.connect(self.add_page)
        self.remove_page_toolB.clicked.connect(self.remove_page)
        self.next_page_toolB.clicked.connect(self.next_page)
        self.back_page_toolB.clicked.connect(self.prev_page)
        self.Browse_ico_diy_toolB.clicked.connect(self.browse_icon_handler)
        self.Browse_ico_lib_toolB.clicked.connect(self.open_ico_library)
        self.app_choice_toolB.clicked.connect(self.open_app_selector)
        self.save_new_pushB.clicked.connect(self.save_new_shortcut_preset)

    def setup_tree_widget(self):
        """Настройка дерева префабов."""
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.show_tree_context_menu)
        self.update_tree_view()

    def set_editor_enabled(self, enabled):
        self.Example_groupB.setEnabled(enabled)
        self.ico_groupB.setEnabled(enabled)
        self.funcrion_widget.setEnabled(enabled)

    def load_stylesheet(self):
        style_path = os.path.join(self.plugin_path, "config", "style_shortcut_bandito.json")
        style_data = load_json(style_path)
        if style_data:
            self.setStyleSheet(parse_style_to_css(style_data))

    def load_actions_config(self):
        self.action_comboB.clear()
        for action in self.manager.get_actions():
            self.action_comboB.addItem(action.get("name"), action)

    def setup_buttons(self):
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(False)
        for i in range(1, 13):
            btn_name = f"butt_toolB_{i:02d}"
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                self.button_group.addButton(btn, i)
                btn.clicked.connect(lambda checked=False, bid=i: self.on_button_toggled(bid))
                btn.setContextMenuPolicy(Qt.CustomContextMenu)
                btn.customContextMenuRequested.connect(lambda pos, b=btn: self.show_context_menu(pos, b))
                btn.setAcceptDrops(True)
                btn.dragEnterEvent = lambda e, b=btn: self.btn_dragEnterEvent(e, b)
                btn.dropEvent = lambda e, b=btn: self.btn_dropEvent(e, b)

    def btn_dragEnterEvent(self, event, btn):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()

    def btn_dropEvent(self, event, btn):
        selected_items = self.treeWidget.selectedItems()
        if not selected_items: return
        
        data = selected_items[0].data(0, Qt.UserRole)
        prefab_name = data.get("prefab_name")
        prefabs = self.manager.get_prefabs()
        
        if prefab_name in prefabs:
            new_btn_data = prefabs[prefab_name].copy()
            self.manager.update_button(self.manager.current_page, btn.objectName(), new_btn_data)
            event.acceptProposedAction()

    def show_context_menu(self, pos, btn):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        if menu.exec(btn.mapToGlobal(pos)) == delete_action:
            self.manager.delete_button(self.manager.current_page, btn.objectName())

    def on_button_toggled(self, btn_id):
        clicked_btn = self.button_group.button(btn_id)
        btn_name = clicked_btn.objectName()
        
        # Звук
        context_map = self.sound_manager.config_map.get("plugins", {}).get("shortcut", {})
        sound_key = context_map.get(btn_name, "button_click")
        self.sound_manager.play(sound_key)

        if clicked_btn.isChecked():
            for btn in self.button_group.buttons():
                if btn is not clicked_btn: btn.setChecked(False)
            self.set_editor_enabled(True)
            self.load_button_settings(btn_name)
            self.update_example_button(btn_name)
        else:
            self.set_editor_enabled(False)
            self.clear_editor_fields()
            self.Example_toolB.setText("...")
            self.Example_toolB.setIcon(QIcon())

    def add_page(self):
        self.sound_manager.play("add_page")
        self.manager.current_page = self.manager.add_new_page()
        self.refresh_page()

    def remove_page(self):
        self.sound_manager.play("remove_page")
        self.manager.current_page = self.manager.remove_page(self.manager.current_page)
        self.refresh_page()

    def next_page(self):
        self.sound_manager.play("button_sw")
        next_page_key = f"page_{self.manager.current_page + 1}"
        if next_page_key in self.manager.get_data():
            self.manager.current_page += 1
            self.refresh_page()

    def prev_page(self):
        if self.manager.current_page > 1:
            self.sound_manager.play("button_sw")
            self.manager.current_page -= 1
            self.refresh_page()

    def save_new_shortcut_preset(self):
        checked_btn = next((btn for btn in self.button_group.buttons() if btn.isChecked()), None)
        if not checked_btn: return
            
        current_tab = self.funcrion_widget.currentIndex()
        name, action_type, action_value = "New Button", "shortcut", ""
        
        if current_tab == 0: # App
            name = self.app_title_lineE.text() or "New App"
            action_value, action_type = self.app_path_lineE.text(), "program"
        elif current_tab == 1: # Shortcut
            name = self.sh_title_lineE.text() or "New Shortcut"
            action_value = self.sh_hc1_keyEdit.keySequence().toString(QKeySequence.SequenceFormat.NativeText)
            action_type = "shortcut"
        elif current_tab == 2: # Action
            name = self.action_title_lineE.text() or "New Action"
            data = self.action_comboB.currentData()
            if data:
                action_type, action_value = data.get("type", "system"), data.get("value", "")

        icon_path = self.current_icon_path or "resources/ico/ico_shortcut.png"
        new_btn_data = {
            "name": name, "icon_path": icon_path, "icon_size": 70,
            "action": {"type": action_type, "value": action_value}
        }
        
        # Диалог сохранения префаба
        dialog = SavePrefabDialog(self, default_name=name)
        if dialog.exec() == QDialog.Accepted:
            prefab_name = dialog.get_prefab_name()
            if prefab_name in self.manager.get_prefabs():
                if QuestionsDialog(self, question_text=f"Overwrite '{prefab_name}'?").exec() != QDialog.Accepted:
                    return
            self.manager.save_prefab(prefab_name, new_btn_data)
            self.manager.update_button(self.manager.current_page, checked_btn.objectName(), new_btn_data)
            self.update_tree_view()

    def refresh_page(self):
        if hasattr(self, 'current_page_lable'):
             self.current_page_lable.setText(f"Page {self.manager.current_page}")
        
        page_data = self.manager.get_data().get(f"page_{self.manager.current_page}", {})
        for i in range(1, 13):
            btn_name = f"butt_toolB_{i:02d}"
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn.blockSignals(True)
                btn.setChecked(False)
                if btn_name in page_data:
                    props = page_data[btn_name]
                    btn.setText("")
                    icon_path = props.get("icon_path")
                    if icon_path and os.path.exists(os.path.join(self.plugin_path, icon_path)):
                        btn.setIcon(QIcon(os.path.join(self.plugin_path, icon_path)))
                        size = props.get("icon_size", 64)
                        from PySide6.QtCore import QSize
                        btn.setIconSize(QSize(size, size))
                    else: btn.setIcon(QIcon())
                else:
                    btn.setText("...")
                    btn.setIcon(QIcon())
                btn.blockSignals(False)

        self.set_editor_enabled(False)
        self.clear_editor_fields()
        self.Example_toolB.setText("...")
        self.Example_toolB.setIcon(QIcon())
        self.back_page_toolB.setEnabled(self.manager.current_page > 1)
        self.next_page_toolB.setEnabled(f"page_{self.manager.current_page + 1}" in self.manager.get_data())
        self.update_tree_view()

    def update_tree_view(self):
        self.treeWidget.clear()
        cats = {
            "program": QTreeWidgetItem(self.treeWidget, ["Application"]),
            "shortcut": QTreeWidgetItem(self.treeWidget, ["Shortcut"]),
            "system": QTreeWidgetItem(self.treeWidget, ["Action"]),
            "action": QTreeWidgetItem(self.treeWidget, ["Action"]),
            "other": QTreeWidgetItem(self.treeWidget, ["Other"])
        }
        for c in cats.values(): c.setExpanded(True)
        
        for name, data in self.manager.get_prefabs().items():
            item = QTreeWidgetItem([name])
            item.setData(0, Qt.UserRole, {"prefab_name": name})
            icon_path = data.get("icon_path")
            if icon_path and os.path.exists(os.path.join(self.plugin_path, icon_path)):
                item.setIcon(0, QIcon(os.path.join(self.plugin_path, icon_path)))
            
            act_type = data.get("action", {}).get("type", "other")
            cats.get(act_type, cats["other"]).addChild(item)

    def browse_icon_handler(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Images (*.png *.jpg *.ico *.svg)")
        if path:
            rel_path = copy_icon_to_plugin(path, self.plugin_path)
            if rel_path:
                self.current_icon_path = rel_path
                from PySide6.QtCore import QSize
                self.Example_toolB.setIcon(QIcon(os.path.join(self.plugin_path, rel_path)))
                self.Example_toolB.setIconSize(QSize(70, 70))

    def open_ico_library(self):
        dialog = IcoListDialog(self, icon_dir=os.path.join(self.plugin_path, "resources", "ico"))
        if dialog.exec():
            rel_path = dialog.get_selected_icon()
            if rel_path:
                self.current_icon_path = rel_path
                from PySide6.QtCore import QSize
                self.Example_toolB.setIcon(QIcon(os.path.join(self.plugin_path, rel_path)))
                self.Example_toolB.setIconSize(QSize(70, 70))

    def load_button_settings(self, btn_name):
        self.clear_editor_fields()
        page_data = self.manager.get_data().get(f"page_{self.manager.current_page}", {})
        btn_data = page_data.get(btn_name, {})
        
        self.current_icon_path = btn_data.get("icon_path")
        name = btn_data.get("name", "")
        for le in [self.app_title_lineE, self.sh_title_lineE, self.action_title_lineE]:
            le.blockSignals(True)
            le.setText(name)
            le.blockSignals(False)
            
        action = btn_data.get("action", {})
        act_type, act_val = action.get("type"), action.get("value")
        
        if act_type == "program": self.app_path_lineE.setText(act_val)
        elif act_type == "shortcut": self.sh_hc1_keyEdit.setKeySequence(QKeySequence(act_val))
        elif act_type == "system":
            for i in range(self.action_comboB.count()):
                if self.action_comboB.itemData(i).get("value") == act_val:
                    self.action_comboB.setCurrentIndex(i)
                    break

    def update_example_button(self, btn_name):
        page_data = self.manager.get_data().get(f"page_{self.manager.current_page}", {})
        btn_data = page_data.get(btn_name, {})
        self.Example_toolB.setText(btn_data.get("name", "..."))
        icon_path = btn_data.get("icon_path")
        if icon_path and os.path.exists(os.path.join(self.plugin_path, icon_path)):
            self.Example_toolB.setIcon(QIcon(os.path.join(self.plugin_path, icon_path)))
            size = btn_data.get("icon_size", 64)
            from PySide6.QtCore import QSize
            self.Example_toolB.setIconSize(QSize(size, size))
        else: self.Example_toolB.setIcon(QIcon())

    def clear_editor_fields(self):
        self.sh_title_lineE.clear()
        self.app_title_lineE.clear()
        self.action_title_lineE.clear()
        self.app_path_lineE.clear()
        self.sh_hc1_keyEdit.clear()

    def handle_button_press(self, *args, **kwargs):
        """Обработка нажатия кнопки от ядра сервера."""
        if args:
            self.manager.handle_remote_press(args[0])

    def open_app_selector(self):
        dialog = AppListDialog(self)
        if dialog.exec():
            path, name = dialog.get_selected_app()
            if path:
                self.app_path_lineE.setText(path)
                if not self.app_title_lineE.text(): self.app_title_lineE.setText(name)

    def show_tree_context_menu(self, pos):
        item = self.treeWidget.itemAt(pos)
        if not item or not item.parent(): return
        
        menu = QMenu(self.treeWidget)
        rename_act, delete_act = menu.addAction("Rename"), menu.addAction("Delete")
        action = menu.exec(self.treeWidget.mapToGlobal(pos))
        
        prefab_name = item.data(0, Qt.UserRole).get("prefab_name")
        if action == delete_act:
            if QuestionsDialog(self, question_text=f"Delete prefab '{prefab_name}'?").exec() == QDialog.Accepted:
                self.manager.delete_prefab(prefab_name)
                self.update_tree_view()
        elif action == rename_act:
            dialog = SavePrefabDialog(self, default_name=prefab_name)
            if dialog.exec() == QDialog.Accepted:
                new_name = dialog.get_prefab_name()
                if new_name != prefab_name:
                    self.manager.rename_prefab(prefab_name, new_name)
                    self.update_tree_view()
