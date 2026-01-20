# El_GUI_Bandito

> Custom Stream Deck analog based on Raspberry Pi 3B+ (Client) and PC (Server).
> Кастомный аналог Stream Deck на базе Raspberry Pi 3B+ (Client) and PC (Server).

[English Version](#english-version) | [Русская версия](#русская-версия)

---

<a name="english-version"></a>
## 🇺🇸 English Version

### 📋 Description
The project consists of two parts:
1.  **Client (RPi):** Python + PySide6 application with a touch interface. Acts as a control panel.
2.  **Server (PC):** FastAPI application on Windows. Receives commands from RPi via WebSocket and manages the system (audio, app launching, key emulation).

### 🏗 Architecture
* **Connection:** Two-way WebSocket.
    * Server: `FastAPI` (Python)
    * Client: `QtWebSockets` (C++ binding)
* **UI:** Qt Designer -> `.ui` files -> auto-compilation to `.py`.
    * Styling via external JSON files (Dark Theme, Network Status).
* **Configuration:** * Settings saved in JSON (separate for Server and Client).
    * Encrypted sensitive data (passwords).
* **Settings:** * Built-in IP and port validation.
    * Network diagnostic tool (Ping) with result parsing and status display.

### 📂 Project Structure
* `el_cliento/` — Client source code (runs on Raspberry Pi).
* `el_bandito/` — Server source code (runs on Windows).
* `src/manager_plugin.py` — Plugin management logic (UI: `plugin_manager.ui`).
* `resources/ui_raw/` — Source design files (.ui).
* `resources/ui_done/` — Compiled files (.py). **Do not edit manually!**

---

<a name="русская-версия"></a>
## 🇷🇺 Русская версия

### 📋 Описание
Проект состоит из двух частей:
1.  **Client (RPi):** Python + PySide6 приложение с сенсорным интерфейсом. Выступает в роли пульта управления.
2.  **Server (PC):** FastAPI приложение на Windows. Принимает команды от RPi по WebSocket и управляет системой (звук, запуск программ, эмуляция нажатий).

### 📸 Интерфейс / UI Screenshots

<table>
  <tr>
    <td align="center"><b>Server Side (PC)</b></td>
    <td align="center"><b>Client Side (RPi)</b></td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/92bd2867-192f-4a17-86d9-bd6efdb25f89" width="450" alt="Server UI" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/5bb80ec0-6cdf-43af-aa88-37c28e0c30c9" width="450" alt="Client UI" />
    </td>
  </tr>
  <tr>
    <td align="center"><i>Интерфейс сервера для управления системой</i></td>
    <td align="center"><i>Сенсорный интерфейс пульта управления</i></td>
  </tr>
</table>

### 🏗 Архитектура
* **Связь:** WebSocket (двусторонняя).
    * Server: `FastAPI` (Python)
    * Client: `QtWebSockets` (C++ binding)
* **UI:** Qt Designer -> `.ui` файлы -> автоматическая компиляция в `.py`.
    * Стилизация через внешние JSON файлы (Dark Theme, Network Status).
* **Конфигурация:** * Сохранение настроек в JSON (раздельно для Server и Client).
    * Шифрование чувствительных данных (паролей).

### 📂 Структура проекта
* `el_cliento/` — Исходный код клиента (Raspberry Pi).
* `el_bandito/` — Исходный код сервера (Windows).
* `src/manager_plugin.py` — Логика управления плагинами.
* `resources/ui_raw/` — Исходные файлы дизайна (.ui).
* `resources/ui_done/` — Скомпилированные файлы (.py). **Не редактировать вручную!**
* `configs/` — Файлы конфигурации JSON.

---

## 🚀 Installation & Launch / Установка и Запуск

### Requirements / Требования
* Python 3.10+
* PySide6
* FastAPI, Uvicorn (for server)

### Launch / Запуск (Dev Mode)
**Server (PC):**
```bash
python el_bandito/el_bandito.py
