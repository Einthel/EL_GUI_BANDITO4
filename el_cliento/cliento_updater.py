import json
import os
import sys
import base64
import logging
import hashlib
from websockets.sync.client import connect

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - UPDATER - %(levelname)s - %(message)s')
logger = logging.getLogger("Updater")

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # папка el_cliento
ROOT_DIR = os.path.dirname(BASE_DIR) # Корневая папка проекта (где лежит el_cliento/)
VER_FILE = os.path.join(BASE_DIR, "ver")
CONFIG_FILE = os.path.join(ROOT_DIR, "configs", "el_cliento_config.json")

# Fallback для конфига, если структура папок отличается (например на RPi)
if not os.path.exists(CONFIG_FILE):
    # Проверяем в текущей директории
    local_config = os.path.join(BASE_DIR, "el_cliento_config.json")
    if os.path.exists(local_config):
        CONFIG_FILE = local_config

class Updater:
    def __init__(self):
        self.server_url = None
        self.dev_mode = False
        self.load_config()

    def load_config(self):
        """Загрузка настроек подключения."""
        # Значения по умолчанию
        ip = "127.0.0.1"
        port = 8000
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Поддержка разных форматов конфига (если ключи отличаются)
                    ip = config.get("ip_destination", config.get("ip", ip))
                    port = config.get("port", config.get("port", port))
                    self.dev_mode = config.get("dev_mode", False)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        else:
            logger.warning(f"Config file not found at {CONFIG_FILE}. Using defaults.")
        
        self.server_url = f"ws://{ip}:{port}/ws"
        logger.info(f"Server URL set to: {self.server_url}, Dev Mode: {self.dev_mode}")

    def get_local_version(self):
        if os.path.exists(VER_FILE):
            try:
                with open(VER_FILE, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except:
                pass
        return "0.0.0"

    def update_local_version(self, version):
        try:
            with open(VER_FILE, 'w', encoding='utf-8') as f:
                f.write(version)
            logger.info(f"Local version updated to {version}")
        except Exception as e:
            logger.error(f"Failed to write version file: {e}")

    def calculate_file_md5(self, filepath):
        """Считает MD5 локального файла."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None

    def calculate_bytes_md5(self, data):
        """Считает MD5 от байтов."""
        return hashlib.md5(data).hexdigest()

    def check_and_update(self):
        """
        Основной метод. 
        Возвращает True, если было обновление и нужен перезапуск.
        Возвращает False, если обновление не требуется или произошла ошибка.
        """
        logger.info("Checking for updates...")
        
        try:
            # Используем контекстный менеджер для соединения
            with connect(self.server_url) as websocket:
                
                # 1. Получаем версию сервера
                websocket.send(json.dumps({"command": "UPDATE_GET_VER"}))
                response = json.loads(websocket.recv())
                
                if response.get("type") != "UPDATE_RESPONSE_VER":
                    logger.error(f"Unexpected response for version check: {response}")
                    return False
                
                server_version = response.get("version")
                local_version = self.get_local_version()
                
                logger.info(f"Local version: {local_version}, Server version: {server_version}")
                
                if server_version == local_version:
                    if self.dev_mode:
                        logger.info("Dev Mode enabled: Forcing manifest check despite version match.")
                    else:
                        logger.info("Client is up to date.")
                        return False
                
                logger.info("Update required. Fetching manifest...")
                
                # 2. Получаем манифест
                websocket.send(json.dumps({"command": "UPDATE_GET_MANIFEST"}))
                response = json.loads(websocket.recv())
                
                if response.get("type") != "UPDATE_RESPONSE_MANIFEST":
                    logger.error("Failed to get manifest")
                    return False
                
                manifest = response.get("manifest")
                if not manifest:
                    logger.error("Empty manifest received")
                    return False

                # 3. Обработка манифеста
                # Создаем папки
                for directory in manifest.get("directories_to_ensure", []):
                    dir_path = os.path.join(ROOT_DIR, directory)
                    os.makedirs(dir_path, exist_ok=True)
                
                # Скачиваем файлы
                files_map = manifest.get("files_map", [])
                total_files = len(files_map)
                files_updated = False # Флаг: были ли изменения файлов
                
                for index, file_info in enumerate(files_map):
                    remote_path = file_info["remote_path"]
                    local_dir_rel = file_info["local_dir"]
                    remote_md5 = file_info.get("md5")
                    
                    # Определяем локальное имя файла
                    filename = os.path.basename(remote_path)
                    local_path = os.path.join(ROOT_DIR, local_dir_rel, filename)
                    
                    # 1. Проверка: нужно ли качать?
                    if os.path.exists(local_path) and remote_md5:
                        local_md5 = self.calculate_file_md5(local_path)
                        if local_md5 == remote_md5:
                            logger.info(f"[{index+1}/{total_files}] {filename} is up to date (MD5 match). Skipping.")
                            continue

                    logger.info(f"Downloading [{index+1}/{total_files}]: {filename}...")
                    
                    websocket.send(json.dumps({
                        "command": "UPDATE_DOWNLOAD_FILE", 
                        "path": remote_path
                    }))
                    
                    file_response = json.loads(websocket.recv())
                    
                    if file_response.get("type") == "UPDATE_RESPONSE_FILE":
                        b64_data = file_response.get("data")
                        file_data = base64.b64decode(b64_data)
                        
                        # 2. Проверка целостности скачанного
                        if remote_md5:
                            downloaded_md5 = self.calculate_bytes_md5(file_data)
                            if downloaded_md5 != remote_md5:
                                logger.error(f"MD5 Mismatch for {filename}! Expected: {remote_md5}, Got: {downloaded_md5}. Aborting.")
                                return False
                        
                        # Записываем файл
                        with open(local_path, "wb") as f:
                            f.write(file_data)
                        files_updated = True # Отмечаем, что было обновление
                    else:
                        logger.error(f"Failed to download {filename}: {file_response.get('message')}")
                        return False
                
                # 4. Обновляем версию локально после успешной загрузки всех файлов
                self.update_local_version(server_version)
                logger.info("Update check completed.")
                
                # Решаем, нужен ли перезапуск
                if server_version != local_version:
                    logger.info("Version changed -> Restart required.")
                    return True
                
                if files_updated:
                    logger.info("Files updated (Dev Mode) -> Restart required.")
                    return True
                
                logger.info("No changes detected -> Launching client.")
                return False

        except Exception as e:
            logger.error(f"Update failed (server might be offline): {e}")
            return False

# Глобальная точка входа
def check_and_update():
    updater = Updater()
    return updater.check_and_update()

if __name__ == "__main__":
    check_and_update()
