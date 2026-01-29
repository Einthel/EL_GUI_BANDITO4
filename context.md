# Technical Brief: El_GUI_Bandito Handover

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
*   **Configuration:** JSON-based settings (`configs/`).
*   **Diagnostics:** Integrated Ping tool.

## Architecture Key Points
*   **Paths:**
    *   `el_bandito/`: Server entry point.
    *   `el_cliento/`: Client entry point.
    *   `plugins/`: Plugin directory. Each plugin has `_manifest.json`, `.ui` files, and `resources/`.
    *   `src/`: Shared modules.
*   **Interaction:**
    *   **Commands:** `UPDATE_PLUGIN_SLOTS`, `SET_ACTIVE_SLOT`, `CLIENT_SET_ACTIVE_SLOT`, `PLUGIN_LIST_ALL`.
    *   Server logs events -> Signals UI updates.

## Key Design Decisions
1.  **Hybrid UI Compilation:** Main App (Source->Dest) vs Plugins (In-Place).
2.  **Manager Pattern:** Logic split into managers (`manager_compile`, `manager_plugin`, `manager_save_load`).
3.  **Non-Blocking Server:** FastAPI in `ServerThread`.
4.  **Optimistic UI:** Client loads plugin UI immediately on click, then notifies server.

## Last Task & Context
*   **Feature:** Implemented full Plugin Slot system (Assign/Delete/Reload).
*   **Feature:** Created `PluginListWindow` for selecting plugins.
*   **Sync:** Implemented bidirectional active plugin synchronization and client-side LED indication.
*   **Update:** Rewrote client plugin updater to discover and download new plugins from server.

## Next Steps
1.  **Plugin Logic:** Implement actual functionality for `Shortcut` plugin (currently just UI).
2.  **New Plugin:** Create `Music` plugin (control system volume/media).
3.  **Refactoring:** Standardize `ElPlugin` base class if needed for complex logic.

