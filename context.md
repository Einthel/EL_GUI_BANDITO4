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
        *   Client downloads new/missing plugins via `cliento_plugin_updater.py`.
        *   **Active State Sync:** Bidirectional switching. Changing plugin on Server updates Client, and vice versa.
    *   **Visuals:**
        *   Server: Dynamic UI loading in `right_frame`. Toggle buttons.
        *   Client: LED indicators for active plugin. Button names update dynamically.
    *   **Plugin Logic Loading:**
        *   Client dynamically loads Python classes from plugin modules.
        *   Plugin classes initialized with WebSocket socket for communication.
*   **Auto-Update System (Manifest-based):**
    *   **Unified Versioning:** Versions are stored directly in JSON manifests (`min_app_version`). Legacy `ver_*` files removed.
    *   **Client Auto-Update:** `cliento_updater.py` uses `cliento_manifest.json` for versioning and file sync.
    *   **Plugin Updates:** `cliento_plugin_updater.py` uses per-plugin manifests (e.g., `shortcut_manifest.json`).
    *   **MD5 Verification:** Dynamic MD5 hashing on server, incremental updates, integrity check.
    *   **Dev Mode:** `dev_mode: true` forces MD5 sync check regardless of version.
    *   **Dynamic Manifests:** `is_directory: true` auto-expands to file list for folder sync.
*   **Plugins:**
    *   **Shortcut:** Multi-page navigation, Prefabs system (`prefab_but_shortcut.json`), AppListDialog (Start Menu scan), live icon/config push (`SHORTCUT_ICON_UPDATE`), safe Qt signal management.
    *   **Music:** Control for Yandex Music (in development).
    *   **Sound/Example:** Template plugins for audio and testing.
*   **Configuration:** JSON-based settings (`configs/`). Password encryption (Base64+XOR).
*   **Diagnostics:** Integrated Ping tool with `cp866` support for Windows.

## Architecture Key Points
*   **Paths:**
    *   `el_bandito/`: Server entry point.
    *   `el_cliento/`: Client entry point.
    *   `plugins/`: Plugin directory. Each plugin has `_manifest.json`, `.ui` files, and `resources/`.
    *   `src/`: Shared modules.
*   **Interaction:**
    *   **Core Commands:** `UPDATE_PLUGIN_SLOTS`, `SET_ACTIVE_SLOT`, `CLIENT_SET_ACTIVE_SLOT`, `PLUGIN_LIST_ALL`.
    *   **Update Commands:** `UPDATE_GET_VER`, `UPDATE_GET_MANIFEST`, `UPDATE_DOWNLOAD_FILE`, `PLUGIN_UPDATE_GET_VER`, `PLUGIN_UPDATE_GET_MANIFEST`.
    *   **Plugin Commands:** `PLUGIN_BUTTON_PRESS` (`page:button_id`), `SHORTCUT_ICON_UPDATE`, `SHORTCUT_CONFIG_UPDATE`.
*   **Delegation:** Server delegates plugin actions via `handle_plugin_action`, dynamically loads plugin server logic.

## Key Design Decisions
1.  **Manifest-based Versioning:** Single source of truth for app and plugin versions within their manifests.
2.  **Client Optimization:** No UI compilation on RPi. Pre-compiled UI (`resources/ui_done`) delivered during update.
3.  **Manager Pattern:** Logic split into `manager_compile`, `manager_plugin`, `manager_save_load`.
4.  **Non-Blocking Server:** FastAPI in `ServerThread`.
5.  **Optimistic UI:** Client loads plugin UI immediately, then notifies server.

## Next Steps
1.  **Music Plugin:** Complete Yandex Music integration logic.
2.  **Refactoring:** Standardize `ElPlugin` base class across all plugins.
3.  **Stability:** Stress test multi-client synchronization and large icon folder sync.

## Technical Nuances
*   **UI Compilation:** `src/manager_compile.py` handles Core (Source->Dest) and Plugins (In-Place).
*   **Server Plugin Loading:** `el_bandito.py` embeds plugin UI in `right_frame`.
*   **Safe Signals:** Shortcut plugin uses `disconnect()` before `connect()` to prevent duplicate signal triggers.
*   **Versioning Source:** `server_main.py` extracts versions dynamically from manifest JSONs.
