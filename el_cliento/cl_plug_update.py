import json
import os
import logging
import base64
from websockets.sync.client import connect

# Импортируем родительский класс Updater
from cl_update import Updater, ROOT_DIR

# Настройка логирования для плагинов
logger = logging.getLogger("PluginUpdater")

class PluginUpdater(Updater):
    def __init__(self):
        super().__init__()
        self.plugins_dir = os.path.join(ROOT_DIR, "plugins")

    def get_installed_plugins(self):
        """Сканирует папку plugins/ и возвращает список ID плагинов (имен папок)."""
        if not os.path.exists(self.plugins_dir):
            return []
        
        plugins = []
        for item in os.listdir(self.plugins_dir):
            full_path = os.path.join(self.plugins_dir, item)
            # Игнорируем файлы и __pycache__
            if os.path.isdir(full_path) and not item.startswith("__") and not item.startswith("."):
                plugins.append(item)
        return plugins

    def get_available_plugins(self, websocket):
        """Запрашивает список всех доступных плагинов с сервера."""
        logger.info("Requesting available plugins list from server...")
        websocket.send(json.dumps({
            "command": "PLUGIN_LIST_ALL"
        }))
        
        response = json.loads(websocket.recv())
        if response.get("type") == "PLUGIN_LIST_RESPONSE":
            return response.get("plugins", [])
        else:
            logger.error(f"Failed to get plugin list: {response}")
            return []

    def get_local_plugin_version(self, plugin_id):
        """Читает версию из манифеста плагина {plugin_id}_manifest.json."""
        manifest_name = f"{plugin_id}_manifest.json"
        manifest_path = os.path.join(self.plugins_dir, plugin_id, manifest_name)
        
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    return manifest.get("min_app_version", "0.0.0")
            except Exception as e:
                logger.error(f"[{plugin_id}] Failed to read manifest for version: {e}")
        return "0.0.0"

    def save_plugin_manifest(self, plugin_id, manifest):
        """Сохраняет манифест плагина локально."""
        manifest_name = f"{plugin_id}_manifest.json"
        manifest_path = os.path.join(self.plugins_dir, plugin_id, manifest_name)
        
        # Убеждаемся, что папка плагина существует
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        
        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            logger.info(f"[{plugin_id}] Manifest saved to {manifest_path}")
        except Exception as e:
            logger.error(f"[{plugin_id}] Failed to save manifest: {e}")

    def update_single_plugin(self, websocket, plugin_id):
        """
        Проверяет и обновляет один плагин.
        Возвращает True, если файлы были изменены.
        """
        try:
            # 1. Запрашиваем версию плагина на сервере
            logger.debug(f"[{plugin_id}] Checking version...")
            websocket.send(json.dumps({
                "command": "PLUGIN_UPDATE_GET_VER",
                "plugin_id": plugin_id
            }))
            
            response = json.loads(websocket.recv())
            if response.get("type") != "UPDATE_RESPONSE_VER":
                logger.warning(f"[{plugin_id}] Unexpected response type: {response.get('type')}")
                return False

            # Если сервер вернул ошибку (например, плагин не найден на сервере)
            if response.get("status") == "error":
                logger.warning(f"[{plugin_id}] Server error: {response.get('message')}")
                return False

            server_version = response.get("version")
            local_version = self.get_local_plugin_version(plugin_id)

            if server_version == local_version and not self.dev_mode:
                return False

            logger.info(f"[{plugin_id}] Update required: {local_version} -> {server_version}")
            logger.info(f"[{plugin_id}] Fetching manifest...")

            # 2. Запрашиваем манифест плагина
            websocket.send(json.dumps({
                "command": "PLUGIN_UPDATE_GET_MANIFEST",
                "plugin_id": plugin_id
            }))
            
            response = json.loads(websocket.recv())
            if response.get("type") != "UPDATE_RESPONSE_MANIFEST":
                logger.error(f"[{plugin_id}] Failed to get manifest")
                return False

            manifest = response.get("manifest")
            if not manifest:
                return False

            # 3. Сохраняем манифест плагина (обновляем локальную версию)
            self.save_plugin_manifest(plugin_id, manifest)

            # 4. Обработка манифеста (аналогично основному апдейтеру)
            # Создаем папки
            for directory in manifest.get("directories_to_ensure", []):
                dir_path = os.path.join(ROOT_DIR, directory)
                os.makedirs(dir_path, exist_ok=True)

            files_map = manifest.get("files_map", [])
            total_files = len(files_map)
            files_updated = False

            manifest_filename = f"{plugin_id}_manifest.json"

            for index, file_info in enumerate(files_map):
                remote_path = file_info["remote_path"]
                local_dir_rel = file_info["local_dir"]
                remote_md5 = file_info.get("md5")

                filename = os.path.basename(remote_path)
                local_path = os.path.join(ROOT_DIR, local_dir_rel, filename)

                # Пропускаем сам манифест, так как мы его уже сохранили
                if filename == manifest_filename:
                    continue

                # Проверка MD5 (Incremental Update)
                if os.path.exists(local_path) and remote_md5:
                    local_md5 = self.calculate_file_md5(local_path)
                    if local_md5 == remote_md5:
                        continue

                # logger.info(f"[{plugin_id}] Downloading {filename} ({index+1}/{total_files})...")

                # Скачиваем файл (используем стандартную команду загрузки файлов, так как пути полные)
                # Важно: сервер должен разрешать скачивание файлов из папки plugins/
                websocket.send(json.dumps({
                    "command": "UPDATE_DOWNLOAD_FILE", 
                    "path": remote_path
                }))

                file_response = json.loads(websocket.recv())
                
                if file_response.get("type") == "UPDATE_RESPONSE_FILE":
                    b64_data = file_response.get("data")
                    file_data = base64.b64decode(b64_data)
                    
                    # Проверка целостности
                    if remote_md5:
                        downloaded_md5 = self.calculate_bytes_md5(file_data)
                        if downloaded_md5 != remote_md5:
                            logger.error(f"[{plugin_id}] MD5 Mismatch for {filename}. Aborting.")
                            return False # Прерываем обновление этого плагина
                    
                    with open(local_path, "wb") as f:
                        f.write(file_data)
                    files_updated = True
                else:
                    logger.error(f"[{plugin_id}] Failed to download {filename}")
                    return False

            if files_updated or server_version != local_version:
                logger.info(f"[{plugin_id}] Updated {total_files} files.")
                return True
            
            return False

        except Exception as e:
            logger.error(f"[{plugin_id}] Update failed: {e}")
            return False

    def check_and_update_plugins(self):
        """
        Проверяет все доступные на сервере плагины.
        Возвращает True, если хотя бы один плагин был обновлен или установлен (требуется рестарт).
        """
        logger.info("Checking for plugin updates...")
        
        any_plugin_updated = False

        try:
            with connect(self.server_url) as websocket:
                # 1. Get list of all available plugins from server
                available_plugins = self.get_available_plugins(websocket)
                if not available_plugins:
                    logger.info("No plugins available on server.")
                    return False
                
                logger.info(f"Available plugins on server: {available_plugins}")

                # 2. Iterate and update/install each
                for plugin_id in available_plugins:
                    # Check if directory exists, if not - create it (implicitly handled by update_single_plugin logic via manifest)
                    # update_single_plugin handles version check (0.0.0 if not exists) and download
                    if self.update_single_plugin(websocket, plugin_id):
                        any_plugin_updated = True
                        
        except Exception as e:
            logger.error(f"Global plugin update check failed: {e}")
            return False

        if any_plugin_updated:
            logger.info("Plugins updated -> Restart required.")
            return True
        
        logger.info("All plugins are up to date.")
        return False

# Глобальная точка входа
def check_and_update_plugins():
    updater = PluginUpdater()
    return updater.check_and_update_plugins()

if __name__ == "__main__":
    check_and_update_plugins()
