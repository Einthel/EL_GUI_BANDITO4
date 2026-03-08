import os
import json
import importlib.util
from PySide6.QtWidgets import QWidget, QToolButton
try:
    from .src.tn_audio_manager import TnAudioManager
except (ImportError, SystemError, ValueError):
    # Фоллбек на прямой импорт, если пакетная структура отличается
    from src.tn_audio_manager import TnAudioManager

class TuneBanditoPlugin(QWidget):
    """Серверная логика плагина Tune."""

    def __init__(self, plugin_path, core=None):
        super().__init__()
        self.plugin_path = plugin_path
        self.core = core
        self.config_path = os.path.join(self.plugin_path, "config", "config_tune.json")
        self.audio_manager = TnAudioManager()
        
        # Изолированный импорт UI
        self.ui = self._load_ui()
        self.ui.setupUi(self)
        
        self._load_config()
        self._apply_styles()
        self._connect_signals()
        self._log_output_devices_on_start()
        # Отправляем актуальный конфиг клиентам при загрузке плагина
        self.broadcast_update()

    def _apply_styles(self):
        """Загрузка и применение стилей из JSON."""
        style_path = os.path.join(self.plugin_path, "config", "style_tune_bandito.json")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)
                css = ""
                for selector, props in style_data.items():
                    props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
                    css += f"{selector} {{ {props_str} }} \n"
                self.setStyleSheet(css)
            except Exception as e:
                print(f"[Tn] Style: {e}")

    def _log_output_devices_on_start(self):
        """Запрос и логирование доступных аудиовыходов при загрузке плагина."""
        try:
            devices = self.audio_manager.refresh_output_devices()
            if devices:
                # Обновляем конфиг актуальным списком выходных устройств
                if not isinstance(getattr(self, "config", None), dict):
                    self.config = {}
                self.config["output_devices"] = devices
                # Текущее устройство по умолчанию — первый элемент списка
                self.config["selected_device"] = devices[0]
                self._write_config_to_disk()
                self._populate_output_device_combos(devices)
            else:
                print("[Tn] No output devices")
        except Exception as e:
            print(f"[Tn] Output devices: {e}")

    def _populate_output_device_combos(self, devices: list[str]):
        """Заполнить комбобоксы списка аудиовыходов (по умолчанию — первый в списке)."""
        # devices уже упорядочены: первым идёт устройство по умолчанию
        combo_names = ["audiD_01_comboB", "audiD_02_comboB"]
        for idx, name in enumerate(combo_names, start=1):
            combo = getattr(self.ui, name, None)
            if combo is None:
                continue
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(devices)
            if not devices:
                combo.setCurrentIndex(-1)
            else:
                if idx == 1:
                    # Первый комбобокс всегда показывает устройство по умолчанию
                    combo.setCurrentIndex(0)
                else:
                    # Для второго — если есть другой вариант, ставим его, иначе оставляем пустым
                    if len(devices) > 1:
                        combo.setCurrentIndex(1)
                    else:
                        combo.setCurrentIndex(-1)
            combo.blockSignals(False)

    def _load_ui(self):
        """Динамический импорт UI для изоляции ресурсов."""
        ui_path = os.path.join(self.plugin_path, "resources", "ui_done", "ui_tune_bandito.py")
        spec = importlib.util.spec_from_file_location("ui_tune_bandito", ui_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Ui_tune_bandito()

    def _load_config(self):
        """Загрузка конфигурации плагина."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def _write_config_to_disk(self):
        """Служебный метод: сохранить конфиг на диск без broadcast."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def _connect_signals(self):
        """Подключение сигналов интерфейса."""
        # Кнопка сохранения аудиоустройств (имя из ui_tune_bandito.py: output_device_save_toolB)
        button = getattr(self.ui, "output_device_save_toolB", None)
        if button is None:
            # Подстраховка: поиск по objectName в дереве виджетов
            button = self.findChild(QToolButton, "output_device_save_toolB")
        if button is not None:
            button.clicked.connect(self.save_config)
        else:
            print("[Tn] output_device_save_toolB not found")

        # Ручная привязка аудиоустройств: комбобоксы не должны иметь одинаковые выбранные элементы
        if hasattr(self.ui, "audiD_01_comboB"):
            self.ui.audiD_01_comboB.currentIndexChanged.connect(
                lambda idx: self._on_output_combo_changed(1, idx)
            )
        if hasattr(self.ui, "audiD_02_comboB"):
            self.ui.audiD_02_comboB.currentIndexChanged.connect(
                lambda idx: self._on_output_combo_changed(2, idx)
            )

    def _on_output_combo_changed(self, slot_index: int, index: int):
        """Гарантировать, что в двух комбобоксах не выбрано одно и то же устройство."""
        devices = self.audio_manager.get_cached_output_devices()
        if not devices or index < 0 or index >= len(devices):
            return

        selected_name = devices[index]

        if slot_index == 1:
            primary_combo = getattr(self.ui, "audiD_01_comboB", None)
            secondary_combo = getattr(self.ui, "audiD_02_comboB", None)
        else:
            primary_combo = getattr(self.ui, "audiD_02_comboB", None)
            secondary_combo = getattr(self.ui, "audiD_01_comboB", None)

        if primary_combo is None or secondary_combo is None:
            return

        # Если второй комбобокс уже показывает тот же девайс — смещаем его на другую позицию
        if secondary_combo.currentText() == selected_name:
            alt_index = -1
            for i, name in enumerate(devices):
                if name != selected_name:
                    alt_index = i
                    break

            secondary_combo.blockSignals(True)
            if alt_index >= 0:
                secondary_combo.setCurrentIndex(alt_index)
            else:
                # Если альтернативы нет (единственное устройство) — оставляем вторую ячейку пустой
                secondary_combo.setCurrentIndex(-1)
            secondary_combo.blockSignals(False)

    def save_config(self):
        """Сохранение конфигурации и уведомление клиентов."""
        self._apply_output_device_selection_to_config()
        self._write_config_to_disk()
        self._apply_selected_device_to_system()
        self.broadcast_update()

    def _apply_output_device_selection_to_config(self):
        """Считать выбор из комбобоксов и зафиксировать его в конфиге."""
        if not isinstance(getattr(self, "config", None), dict):
            self.config = {}

        # Базовый список устройств (автообновляемый при старте)
        devices = self.audio_manager.get_cached_output_devices()
        if not isinstance(devices, list):
            devices = []

        # Текущий выбор в комбобоксах
        combo1 = getattr(self.ui, "audiD_01_comboB", None)
        combo2 = getattr(self.ui, "audiD_02_comboB", None)

        selected1 = combo1.currentText().strip() if combo1 is not None else ""
        selected2 = combo2.currentText().strip() if combo2 is not None else ""

        # Гарантируем уникальность и порядок: сначала выбор из combo1, затем combo2
        ordered_devices = []

        for name in (selected1, selected2):
            if name and name in devices and name not in ordered_devices:
                ordered_devices.append(name)

        # Добавляем остальные устройства в хвост, сохраняя автообнаруженный список
        for name in devices:
            if name not in ordered_devices:
                ordered_devices.append(name)

        # Обновляем конфиг
        self.config["output_devices"] = ordered_devices
        if ordered_devices:
            # Первый элемент трактуем как "выбранное по умолчанию" устройство
            self.config["selected_device"] = ordered_devices[0]

    def _apply_selected_device_to_system(self):
        """Применить выбранное в конфиге устройство как системное по умолчанию."""
        if not isinstance(getattr(self, "config", None), dict):
            return

        selected = self.config.get("selected_device") or ""
        if not selected:
            print("[Tn] No selected_device")
            return

        ok = self.audio_manager.set_default_output_device(selected)
        if not ok:
            print(f"[Tn] Failed: {selected}")

    def handle_button_press(self, btn_id, _payload=None):
        """Обязательный метод для обработки событий от клиента (PLUGIN_BUTTON_PRESS)."""
        # Специальная обработка кнопок выбора устройства на клиенте
        if btn_id == "audiD_01_toolB":
            self._select_device_by_index(0)
        elif btn_id == "audiD_02_toolB":
            self._select_device_by_index(1)

    def _select_device_by_index(self, index: int):
        """Выбрать устройство по индексу в config['output_devices'], применить и разослать."""
        if not isinstance(getattr(self, "config", None), dict):
            self.config = {}

        devices = self.config.get("output_devices") or []
        if not devices or index < 0 or index >= len(devices):
            print(f"[Tn] No device @{index}")
            return

        selected = devices[index]
        self.config["selected_device"] = selected
        # Применяем к системе, сохраняем и шлем обновление клиентам
        self._write_config_to_disk()
        self._apply_selected_device_to_system()
        self.broadcast_update()

    def broadcast_update(self):
        """Рассылка обновлений всем подключенным клиентам через Core."""
        if not self.core or not self.core.com:
            print("[Tn] No core")
            return
        try:
            self.core.com.broadcast("TUNE_CONFIG_UPDATE", self.config)
        except Exception as e:
            print(f"[Tn] Broadcast: {e}")
