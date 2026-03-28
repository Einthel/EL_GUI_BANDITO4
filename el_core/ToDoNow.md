# Инструкция по добавлению звуков для кнопок (bind_buttons)

Для того чтобы кнопки в новом плагине или окне автоматически издавали звуки при нажатии, следуйте этой инструкции.

## Шаг 1: Подготовка звуковых файлов
1. Поместите файлы `.wav` или `.mp3` в папку `resources/sounds/` в корне проекта.
2. Убедитесь, что в имени файла **нет лишних точек** (правильно: `my_sound.wav`, неправильно: `my_sound..wav`).
3. Имя звука в системе будет соответствовать имени файла без расширения (например, `click`).

## Шаг 2: Регистрация в конфиге
Отредактируйте файл `configs/el_sound_config.json`:
1. Найдите или создайте секцию для вашего плагина/окна.
2. Добавьте соответствие `objectName` кнопки и имени звука.

**Пример для плагина:**
```json
"plugins": {
  "my_plugin_id": {
    "save_toolB": "click",
    "delete_pushB": "delete_sound"
  }
}
```

## Шаг 3: Инициализация в коде плагина (Python)
В методе `__init__` вашего плагина добавьте следующий код:

```python
# 1. Импорт и инициализация менеджера
from el_core.el_sound_manager import ElSoundManager
self.sound_manager = ElSoundManager(self)

# 2. Загрузка общего конфига звуков
# Путь вычисляется относительно папки плагина до папки configs в корне
sound_cfg_path = os.path.join(os.path.dirname(os.path.dirname(self.plugin_path)), "configs", "el_sound_config.json")
self.sound_manager.load_config(sound_cfg_path)

# 3. Привязка звуков к кнопкам (автоматически по objectName)
# context должен совпадать с ключом в JSON (например, "plugins" -> "my_plugin_id")
self.sound_manager.bind_buttons(self, context="plugins/my_plugin_id")
```

## Шаг 4: Ручное воспроизведение (если нужно)
Если кнопка создается динамически или звук нужен в специфическом месте:
```python
self.sound_manager.play("имя_звука")
```

---
*Примечание: Метод `bind_buttons` сканирует все дочерние QPushButton и QToolButton внутри переданного контейнера и подключает их сигнал `clicked` к проигрыванию звука, если их `objectName` найден в конфиге.*
