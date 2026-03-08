import os
import json
from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect, QMediaDevices
from PySide6.QtWidgets import QPushButton, QToolButton

class ElSoundManager(QObject):
    """
    Универсальный менеджер звуков.
    Использует QSoundEffect для минимальной задержки.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sounds = {}
        self.config_map = {}
        self._enabled = True
        self._volume = 0.5
        
        # Проверка наличия аудиоустройств и лог выбранного вывода
        outputs = QMediaDevices.audioOutputs()
        self._has_audio = len(outputs) > 0
        if not self._has_audio:
            self._enabled = False
            return
        default_out = QMediaDevices.defaultAudioOutput()
        if default_out:
            # Qt не отдаёт имя бэкенда (Pulse/ALSA/PipeWire), только устройство
            print(f"[SoundManager] Audio outputs: {len(outputs)}, default: {default_out.description()!r}")
        else:
            print(f"[SoundManager] Audio outputs: {len(outputs)}, default: (none)")

        # Автоматическая загрузка базовых звуков
        self.load_base_sounds()

    def load_config(self, config_path):
        """Загружает карту звуков из JSON."""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_map = json.load(f)
            except Exception:
                self.config_map = {}

    def load_base_sounds(self):
        """Загружает стандартные звуки из resources/sounds."""
        if not self._has_audio:
            return
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "sounds")
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.endswith((".wav", ".mp3")):
                    name = os.path.splitext(file)[0]
                    self.add_sound(name, os.path.join(base_path, file))

    def add_sound(self, name, file_path):
        """Добавляет звук в коллекцию."""
        if not self._has_audio or not os.path.exists(file_path):
            return
            
        effect = QSoundEffect(self)
        effect.setSource(QUrl.fromLocalFile(file_path))
        effect.setVolume(self._volume)
        self.sounds[name] = effect

    def play(self, name):
        """Воспроизводит звук по имени."""
        if not self._enabled or not self._has_audio:
            return
            
        if name in self.sounds:
            effect = self.sounds[name]
            if effect.isPlaying():
                effect.stop()
            effect.play()
        else:
            print(f"[SoundManager] Sound not found: '{name}'")

    def play_file(self, file_path):
        """Воспроизводит звук напрямую из файла (без кэширования в self.sounds)."""
        if not self._enabled or not self._has_audio or not os.path.exists(file_path):
            return
            
        # Создаем временный эффект (Qt сам очистит его, если привязать к parent или использовать deleteLater)
        effect = QSoundEffect(self)
        effect.setSource(QUrl.fromLocalFile(file_path))
        effect.setVolume(self._volume)
        effect.play()

    def bind_buttons(self, container, context="ui_main"):
        """Автоматически привязывает звуки к кнопкам в контейнере."""
        if not self._enabled or not self._has_audio:
            return

        # findChildren не принимает кортеж типов в PySide6, нужно искать отдельно
        buttons = container.findChildren(QPushButton)
        buttons.extend(container.findChildren(QToolButton))
        
        context_map = self.config_map.get(context, {})
        
        for btn in buttons:
            obj_name = btn.objectName()
            if obj_name in context_map:
                sound_name = context_map[obj_name]
                # Используем lambda с захватом переменной sound_name
                btn.clicked.connect(lambda checked=False, s=sound_name: self.play(s))

    def set_enabled(self, enabled):
        """Включение/выключение звуков."""
        if not self._has_audio:
            self._enabled = False
            return
        self._enabled = enabled

    def set_volume(self, volume):
        """Установка громкости (0.0 - 1.0)."""
        if not self._has_audio:
            return
        self._volume = max(0.0, min(1.0, volume))
        for effect in self.sounds.values():
            effect.setVolume(self._volume)
