# El_GUI_Bandito

Кастомный аналог Stream Deck на базе Raspberry Pi 3B+ (Client) и PC (Server).

## 📋 Описание
Проект состоит из двух частей:
1.  **Client (RPi):** Python + PySide6 приложение с сенсорным интерфейсом. Выступает в роли пульта управления.
2.  **Server (PC):** FastAPI приложение на Windows. Принимает команды от RPi по WebSocket и управляет системой (звук, запуск программ, эмуляция нажатий).

### 📸 Интерфейс / UI Screenshots

<table>
  <tr>
    <td align="center"><b>Server Shortcut Side (PC)</b></td>
    <td align="center"><b>Client Shortcut Side (RPi)</b></td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/e3561994-178d-440f-ad2d-c51d03104edb" width="450" alt="Server Shortcut UI" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/e2561388-f7b4-4139-8790-993b9836f72b" width="450" alt="Client Shortcut UI" />
    </td>
  </tr>
  <tr>
    <td align="center"><i>Интерфейс сервера с плагином Shortcut для управления системой</i></td>
    <td align="center"><i>Сенсорный интерфейс клиента плагина Shortcut</i></td>
  </tr>
  <tr>
    <td align="center"><b>Server Tune Side (PC)</b></td>
    <td align="center"><b>Client Tune Side (RPi)</b></td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/211d3ca5-dda5-4b1c-b559-cd0d3c8b7daa" width="450" alt="Server Tune UI" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/45f7f9fa-3f9e-43d7-b14c-9403f7abf749" width="450" alt="Client Tune UI" />
    </td>
  </tr>
    <tr>
    <td align="center"><i>Интерфейс сервера с плагином Tune для управления звуком</i></td>
    <td align="center"><i>Сенсорный интерфейс клиента плагина Tune</i></td>
  </tr>
</table>

## 🏗 Архитектура
*   **Ядро (ElCore):**
    *   **ElStateManager** — конфигурация слотов, активные плагины, кэш инстансов в RAM (JSON).
    *   **ElComManager** — обертка над WebSocket для broadcast и сетевых событий.
    *   **Plugin Life Cycle:** плагины загружаются один раз, при переключении вкладок сохраняют состояние в памяти.
    *   **Core Injection:** плагины могут принимать `core` и использовать `core.com.broadcast()` для рассылки.
*   **Связь:** WebSocket (двусторонняя).
    *   Server: `FastAPI` (Python)
    *   Client: `QtWebSockets` (C++ binding) для команд, `websockets` (Python) для обновлений.
*   **UI:** Qt Designer -> `.ui` файлы -> автоматическая компиляция в `.py` (только на сервере).
    *   Стилизация через внешние JSON файлы (Dark Theme, Network Status).
*   **Звук (ElSoundManager):**
    *   Централизованный менеджер на базе `QSoundEffect`; проверка аудиоустройств (`QMediaDevices`), при отсутствии — тихий режим.
    *   Индивидуальные звуки кнопок через `configs/el_sound_config.json` (привязка по `objectName`); метод `bind_buttons(container, context)` для плагинов.
    *   Раздельное управление: звук сервера (`sound_bandito_checkB` в настройках) и звук клиентов (`sound_checkB`); синхронизация по `UPDATE_SOUND_SETTINGS`.
*   **Система Плагинов (Plugin System):**
    *   **5 Слотов:** Назначение плагинов на слоты через UI сервера.
    *   **Hot Reload / Delete:** Управление плагинами без перезапуска.
    *   **Sync:** Автоматическая синхронизация состава слотов и активного плагина между PC и RPi.
    *   **Auto-Update:** Клиент скачивает назначенные плагины; версии в манифестах (`min_app_version`).
    *   **Плагин Shortcut:**
        *   **Редактор кнопок (сервер):** создание и удаление страниц (`+`/`-`), навигация по страницам, сохранение в `button_shortcut.json` (Save Change), пресеты по имени и хоткею (Save Preset). Панель настроек и кнопка предпросмотра привязаны к выбранной кнопке.
        *   **Типы действий:** вкладка **Application** — выбор программы из меню «Пуск» (диалог `AppListDialog`), кнопки типа `program` с путём и отображаемым именем; вкладка **Shortcut** — эмуляция нажатий клавиш (`keyboard`); вкладка **Action** — системные действия «Page Prev» / «Page Next».
        *   **Иконки:** поддержка форматов `.png`, `.jpg`, `.ico`, `.svg`. Контекстное меню кнопки: «Delete» — очистка конфигурации.
        *   **Prefabs:** библиотека шаблонов кнопок (`prefab_but_shortcut.json`). Дерево по категориям (Application, Shortcut, Action, Other). Сохранение кнопки как шаблона (`SavePrefabDialog`), проверка уникальности имени, контекстное меню: удаление и переименование.
        *   **Live Sync:** мгновенная отправка конфига (`SHORTCUT_CONFIG_UPDATE`) и новых иконок (`SHORTCUT_ICON_UPDATE`) на клиент без перезагрузки приложения.
        *   **Клиент:** динамическое создание страниц и кнопок по конфигурации, локальная навигация по страницам (без запросов к серверу). Стили кнопок через `style_shortcut.json` (Checked/Pressed).
    *   **Плагин Tune:**
        *   Панель быстрых команд для управления звуком ПК (громкость, mute и т.д.). Рассылка команд через `core.com.broadcast()`.
*   **Система обновлений (OTA-like):**
    *   Версии хранятся в JSON-манифестах (`min_app_version`); отдельные файлы версий не используются.
    *   Клиент при запуске проверяет версию на сервере; сервер отдает манифест и измененные файлы (в т.ч. рекурсивно для директорий).
    *   Клиент скачивает готовые `.py` и ресурсы (звуки, иконки), затем перезапускается; проверка целостности по MD5.
    *   **Оптимизация:** На клиенте удалена компиляция UI для ускорения запуска на RPi.
    *   **Dev Mode:** Принудительная синхронизация по MD5 без смены версии (в конфиге `dev_mode: true`).
*   **Конфигурация:** 
    *   Сохранение настроек в JSON (раздельно для Server и Client).
    *   Шифрование чувствительных данных (паролей).

## 📂 Структура проекта
*   `el_core/` — ядро: `el_core.py` (ElCore, оркестратор), `el_state_manager.py`, `el_com_manager.py`, `el_sound_manager.py`.
*   `el_cliento/` — исходный код клиента (Raspberry Pi).
    *   `cl_update.py` — автообновление ядра; `cl_plug_update.py` — обновление плагинов.
    *   `cliento_manifest.json` — манифест и версия (`min_app_version`) для синхронизации.
*   `el_bandito/` — исходный код сервера (Windows).
*   `src/manager_plugin.py` — логика управления плагинами (UI: `plugin_manager.ui`).
*   `resources/ui_raw/` — исходные .ui; `resources/ui_done/` — скомпилированные .py (**не редактировать вручную**); `resources/sounds/` — системные звуки.
    *   `ui_bandito/`, `ui_cliento/` — UI сервера и клиента.
*   `src/utilts.py` — общие утилиты.
*   `configs/` — JSON конфиги (в т.ч. `el_sound_config.json` для озвучки кнопок).
*   `plugins/shortcut/` — плагин Shortcut:
    *   `shortcut_bandito.py`, `shortcut_cliento.py`; манифест `shortcut_manifest.json`.
    *   `config/` — `button_shortcut.json`, `prefab_but_shortcut.json`, `config_shortcut.json`, `style_shortcut.json`.
*   `plugins/tune/` — плагин Tune (управление звуком ПК): `tune_manifest.json`, серверная/клиентская логика и UI в `src/`, `config/`.

## 🔌 Плагины

### Shortcut
Редактор кнопок и пресетов для запуска приложений, эмуляции горячих клавиш и навигации по страницам.

*   **Сервер (Bandito):**
    *   Архитектура: UI (`shortcut_bandito.py`), бизнес-логика (`sh_bandito_manager.py`), сервисы I/O и broadcast (`sh_bandito_service.py`). Синхронизация с клиентами через `core.com.broadcast("SHORTCUT_ICON_UPDATE"|"SHORTCUT_CONFIG_UPDATE", data)`.
    *   Редактор: страницы (+/–), навигация, сохранение в `button_shortcut.json` (Save Change); пресеты по имени и хоткею (Save Preset). Панель настроек и кнопка предпросмотра привязаны к выбранной кнопке.
    *   Типы действий: **Application** — выбор из меню «Пуск» (`AppListDialog`), кнопки `program` с путём и отображаемым именем; **Shortcut** — эмуляция клавиш (`keyboard`); **Action** — «Page Prev» / «Page Next».
    *   Иконки: `.png`, `.jpg`, `.ico`, `.svg`. Контекстное меню кнопки: «Delete» — сброс конфигурации.
    *   Префабы: дерево по категориям (Application, Shortcut, Action, Other) в `prefab_but_shortcut.json`; сохранение кнопки как шаблона (`SavePrefabDialog`), проверка уникальности имени; контекстное меню — удаление и переименование.
*   **Клиент (Cliento):**
    *   Архитектура: UI (`shortcut_cliento.py`), логика и сокеты (`sh_cliento_manager.py`), I/O (`sh_cliento_service.py`). Безопасное управление сигналами Qt и EventFilter для анимации.
    *   Динамическое создание страниц и кнопок по конфигурации; локальная навигация (Page Prev/Next) без запросов к серверу.
    *   Стили: `style_shortcut.json` (Checked/Pressed); `style_shortcut_cliento.json` — анимация «вдавливания» кнопок (QPropertyAnimation: `duration`, `scale_factor`, `easing_curve`).
    *   Звук: привязка через `el_sound_config.json` и опционально `sound_path` в кнопке; fallback — `button_click.wav`. Учёт глобального включения/выключения звука из конфигов сервера и клиента.
*   **Live Sync:** при сохранении — мгновенная отправка конфига и новых иконок на клиент; применение без перезапуска.

### Tune
Панель быстрых команд для управления звуком ПК: громкость, mute, переключение устройств вывода.

*   **Сервер (Bandito):**
    *   Конструктор `TuneBanditoPlugin(plugin_path, core=None)`; рассылка через `core.com.broadcast("TUNE_CONFIG_UPDATE", self.config)` (при отсутствии `core` — предупреждение, broadcast не выполняется).
    *   Аудиоустройства: автоопределение активного вывода при запуске; список устройств и текущее (`selected_device`) в `config_tune.json`. Комбобоксы для двух слотов с уникальностью выбора; сохранение привязки по кнопке `output_device_save_toolB`. Переключение системного устройства вывода через `libs.audio_manager.audioSwitch`.
    *   Стили: `style_tune_bandito.json`; поддержка `qproperty-icon` и `qproperty-iconSize` в JSON.
*   **Клиент (Cliento):**
    *   UI: громкость, микрофон, звук, прочие mute; иконки кнопок (`mic_mute_toolB`, `sound_mute_toolB`, `other_mute_toolB`) подгружаются через стили.
    *   Обработка `TUNE_CONFIG_UPDATE`: сохранение конфига на диск, сигнал `config_updated`. Поля `audiD_01_lineE`, `audiD_02_lineE` заполняются из `config_tune.json` (ключ `output_devices`); подсветка выбранного устройства — dynamic property `selectedDevice`, стиль в `style_tune_cliento.json`.
    *   Кнопки выбора устройства `audiD_01_toolB`, `audiD_02_toolB` отправляют `PLUGIN_BUTTON_PRESS`; сервер по индексу (0/1) устанавливает устройство по умолчанию, сохраняет конфиг и рассылает обновление.

## 🚀 Установка и Запуск

### Требования
*   Python 3.10+
*   PySide6
*   FastAPI, Uvicorn (для сервера)
*   websockets (для клиента)

### Запуск (Dev Mode)
При запуске `el_bandito.py` система автоматически проверит и перекомпилирует изменившиеся `.ui` файлы.
Клиент (`el_cliento.py`) при запуске попытается обновиться с сервера.

**Server (PC):**
```bash
python el_bandito/el_bandito.py
```

**Client (RPi):**
```bash
python el_cliento/el_cliento.py
```
