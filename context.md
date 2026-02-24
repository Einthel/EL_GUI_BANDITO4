# Technical Brief: El_GUI_Bandito Handover

## In short
*   Custom "Stream Deck": RPi as touch controller, PC as execution server.
*   Stack: Python 3.10+, PySide6, WebSocket (JSON). Server: FastAPI/Uvicorn in QThread; client: QWebSocket.
*   Server — `el_bandito/`, client — `el_cliento/`, plugins — `plugins/` (manifest `_manifest.json`), shared — `src/`.
*   Client updates on startup: `cliento_updater.py`, manifest + MD5, restart if needed.
*   Plugins updated separately: `cliento_plugin_updater.py`, bootstrap from main manifest, then per-plugin manifest.

## Project Essence
**El_GUI_Bandito** is a custom client-server "Stream Deck" system using a Raspberry Pi as a touch controller and a PC as the execution server.

**Tech Stack:**
*   **Server (PC/Windows):** Python 3.10+, FastAPI, Uvicorn, PySide6 (UI).
*   **Client (RPi):** Python 3.10+, PySide6 (UI), QtWebSockets.
*   **Communication:** WebSocket (JSON payload).

## Current State
*   **Core Communication:** Bidirectional WebSocket link implemented. Server runs FastAPI in a `QThread`. Client uses `QWebSocket`.
*   **UI System:** Automated pipeline via `src/manager_compile.py`.
*   **Plugin System (V1):** 
    *   **Management:** 5 configurable slots. Assign, Delete, Hot Reload plugins via Server UI.
    *   **Selection:** Modal window (`PluginListWindow`) scanning `plugins/` with manifest reading (`_manifest.json`).
    *   **Storage:** Assignments saved in `configs/el_plugin_config.json`.
    *   **Synchronization:**
        *   Server broadcasts slot config to clients.
        *   Client downloads new/missing plugins via `cliento_plugin_updater.py` (fetching list from server).
        *   **Active State Sync:** Bidirectional switching. Changing plugin on Server updates Client, and vice versa.
    *   **Visuals:**
        *   Server: Dynamic UI loading in `right_frame`. Toggle buttons.
        *   Client: LED indicators for active plugin. Button names update dynamically.
    *   **Plugin Logic Loading:**
        *   Client dynamically loads Python classes (not just UI files) from plugin modules.
        *   Plugin classes initialized with WebSocket socket for communication.
        *   Fallback mechanism for legacy plugins (UI-only).
    *   **Shortcut Plugin:** Prefabs, pages, program/shortcut actions, icons, AppListDialog, live-update of icons and config. See `plugins/shortcut/README.md`.
*   **Auto-Update System:**
    *   **Client Auto-Update:** Automatic client update on startup via `cliento_updater.py`.
    *   **MD5 Verification:** Dynamic MD5 hashing on server, incremental updates (skip if hash matches), integrity check before disk write.
    *   **Dev Mode:** `dev_mode: true` in client config ignores version match, forces MD5 sync check on every startup.
    *   **Manifest System:** `cliento_manifest.json` describes files/directories to sync. Dynamic manifest generation with `is_directory: true` directive (auto-expands to file list).
    *   **Plugin Updates:** Independent plugin update system via `cliento_plugin_updater.py`. Bootstrap mechanism for new plugins via main manifest.
    *   **Version Files:** Conflict resolution: `plugins/shortcut/ver` -> `ver_shortcut`, `el_cliento/ver` -> `ver_cliento`.
*   **Configuration:** JSON-based settings (`configs/`). Password encryption.
*   **Diagnostics:** Integrated Ping tool.

## Architecture Key Points
*   **Paths:**
    *   `el_bandito/`: Server entry point.
    *   `el_cliento/`: Client entry point.
    *   `plugins/`: Plugin directory. Each plugin has `_manifest.json`, `.ui` files, and `resources/`.
    *   `src/`: Shared modules.
*   **Interaction:**
    *   **Core Commands:** `UPDATE_PLUGIN_SLOTS`, `SET_ACTIVE_SLOT`, `CLIENT_SET_ACTIVE_SLOT`, `PLUGIN_LIST_ALL`.
    *   **Update Commands:** `UPDATE_GET_VER`, `UPDATE_GET_MANIFEST`, `UPDATE_DOWNLOAD_FILE`, `PLUGIN_UPDATE_GET_VER`, `PLUGIN_UPDATE_GET_MANIFEST`.
    *   **Plugin Commands:** `PLUGIN_BUTTON_PRESS` (format: `page:button_id`), `SHORTCUT_ICON_UPDATE`, `SHORTCUT_CONFIG_UPDATE`.
    *   **Delegation:** Server delegates plugin actions via `handle_plugin_action`, dynamically loads plugin server logic.
    *   Server logs events -> Signals UI updates.

## Key Design Decisions
1.  **Hybrid UI Compilation:** Main App (Source->Dest) vs Plugins (In-Place).
2.  **Client Optimization:** No UI compilation on client (RPi). Client receives pre-compiled UI (`resources/ui_done`) from server during update. Reduces startup time, eliminates dev dependencies on client.
3.  **Manager Pattern:** Logic split into managers (`manager_compile`, `manager_plugin`, `manager_save_load`).
4.  **Non-Blocking Server:** FastAPI in `ServerThread`.
5.  **Optimistic UI:** Client loads plugin UI immediately on click, then notifies server.
6.  **Dynamic Manifest Generation:** Server auto-expands `is_directory: true` to file list, enabling folder sync (e.g., icons) without explicit enumeration.

## Next Steps
1.  **New Plugin:** Create `Music` plugin (control system volume/media).
2.  **Refactoring:** Standardize `ElPlugin` base class if needed for complex logic.
3.  **Testing:** Verify prefab system, live updates, and multi-page navigation stability.

## Technical Nuances
*   **UI Compilation:** `src/manager_compile.py` handles two modes:
    *   *Core:* `resources/ui_raw/*.ui` -> `resources/ui_done/ui_*.py`.
    *   *Plugins:* `plugins/*/resources/ui_raw/*.ui` -> `plugins/*/resources/ui_done/ui_*.py` (or In-Place if no resources folder).
*   **Server Plugin Loading:** `el_bandito.py` looks for a class inheriting from `QWidget` in `[plugin_name]_bandito.py` to embed in `right_frame`.
*   **Shortcut Live Update:** Uses `SHORTCUT_ICON_UPDATE` and `SHORTCUT_CONFIG_UPDATE` commands for instant client refresh.
*   **Shortcut Prefabs:** Library stored in `plugins/shortcut/config/prefab_but_shortcut.json`.