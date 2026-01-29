import json
import os
import base64
import hashlib
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

def calculate_file_md5(filepath):
    """Вычисляет MD5 хеш файла."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None

class ConnectionManager:
    """
    Класс для управления WebSocket соединениями.
    Позволяет хранить список активных клиентов, отправлять им сообщения
    и рассылать широковещательные уведомления.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Если соединение мертвое, удаляем его (хотя disconnect должен был сработать)
                pass

# Создаем экземпляр менеджера
manager = ConnectionManager()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from typing import List, Dict, Any
import uvicorn

# ... existing code ...

# Создаем приложение FastAPI
app = FastAPI()

# Модель для broadcast сообщения
from pydantic import BaseModel

class BroadcastMessage(BaseModel):
    command: str
    data: Dict[str, Any] = None

@app.post("/api/broadcast")
async def broadcast_endpoint(message: BroadcastMessage):
    """Endpoint для отправки широковещательных сообщений всем клиентам."""
    payload = json.dumps({"command": message.command, "data": message.data})
    await manager.broadcast(payload)
    return {"status": "ok", "message": "Broadcasted"}

# Глобальный обработчик команд (будет переопределен из GUI)
# Это callback функция, которую мы вызовем, когда придет сообщение
command_handler = None

def set_command_handler(handler):
    global command_handler
    command_handler = handler

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Уведомляем систему (через лог/handler), что клиент подключен
    if command_handler:
        command_handler("client_connected", {"ip": websocket.client.host})
        
    try:
        while True:
            # Ожидаем сообщение от клиента
            data = await websocket.receive_text()
            
            # Пытаемся распарсить JSON
            try:
                json_data = json.loads(data)
                
                # --- UPDATE LOGIC START ---
                command = json_data.get("command")
                
                if command == "UPDATE_GET_VER":
                    ver_path = os.path.join("el_cliento", "ver")
                    if os.path.exists(ver_path):
                        with open(ver_path, "r", encoding="utf-8") as f:
                            version = f.read().strip()
                        await manager.send_personal_message(json.dumps({
                            "type": "UPDATE_RESPONSE_VER",
                            "version": version
                        }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": "Version file not found on server"
                        }), websocket)
                    continue

                elif command == "UPDATE_GET_MANIFEST":
                    manifest_path = os.path.join("el_cliento", "cliento_manifest.json")
                    if os.path.exists(manifest_path):
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            manifest = json.load(f)
                        
                        # Calculate MD5 for each file in the manifest
                        if "files_map" in manifest:
                            for file_info in manifest["files_map"]:
                                remote_path = file_info.get("remote_path")
                                full_path = os.path.join(os.getcwd(), remote_path)
                                
                                md5 = calculate_file_md5(full_path)
                                file_info["md5"] = md5

                        await manager.send_personal_message(json.dumps({
                            "type": "UPDATE_RESPONSE_MANIFEST",
                            "manifest": manifest
                        }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": "Manifest file not found on server"
                        }), websocket)
                    continue
                
                elif command == "PLUGIN_LIST_ALL":
                    # Возвращает список всех доступных плагинов на сервере
                    plugins_dir = os.path.join(os.getcwd(), "plugins")
                    available_plugins = []
                    
                    if os.path.exists(plugins_dir):
                        for item in os.listdir(plugins_dir):
                            full_path = os.path.join(plugins_dir, item)
                            if os.path.isdir(full_path) and not item.startswith("__") and not item.startswith("."):
                                # Check if it looks like a valid plugin (has manifest or py files)
                                available_plugins.append(item)
                    
                    await manager.send_personal_message(json.dumps({
                        "type": "PLUGIN_LIST_RESPONSE",
                        "plugins": available_plugins
                    }), websocket)
                    continue

                elif command == "PLUGIN_UPDATE_GET_VER":
                    plugin_id = json_data.get("plugin_id")
                    # Security check for plugin_id
                    if not plugin_id or ".." in plugin_id or "/" in plugin_id or "\\" in plugin_id:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": "Invalid plugin ID"
                        }), websocket)
                        continue

                    ver_path = os.path.join("plugins", plugin_id, "ver")
                    if os.path.exists(ver_path):
                        with open(ver_path, "r", encoding="utf-8") as f:
                            version = f.read().strip()
                        await manager.send_personal_message(json.dumps({
                            "type": "UPDATE_RESPONSE_VER",
                            "version": version,
                            "plugin_id": plugin_id
                        }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "status": "error",
                            "message": f"Version file not found for plugin: {plugin_id}"
                        }), websocket)
                    continue

                elif command == "PLUGIN_UPDATE_GET_MANIFEST":
                    plugin_id = json_data.get("plugin_id")
                    if not plugin_id or ".." in plugin_id:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": "Invalid plugin ID"
                        }), websocket)
                        continue

                    # Стандартизированное имя манифеста: {plugin_id}_manifest.json
                    manifest_name = f"{plugin_id}_manifest.json"
                    manifest_path = os.path.join("plugins", plugin_id, manifest_name)
                    
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, "r", encoding="utf-8") as f:
                                manifest = json.load(f)
                            
                            # Динамический расчет MD5 для файлов плагина
                            if "files_map" in manifest:
                                for file_info in manifest["files_map"]:
                                    remote_path = file_info.get("remote_path")
                                    # Важно: remote_path должен быть относительным от корня проекта
                                    full_path = os.path.join(os.getcwd(), remote_path)
                                    
                                    md5 = calculate_file_md5(full_path)
                                    file_info["md5"] = md5

                            await manager.send_personal_message(json.dumps({
                                "type": "UPDATE_RESPONSE_MANIFEST",
                                "manifest": manifest,
                                "plugin_id": plugin_id
                            }), websocket)
                        except Exception as e:
                            await manager.send_personal_message(json.dumps({
                                "type": "error",
                                "message": f"Error processing manifest: {str(e)}"
                            }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": f"Manifest not found for plugin: {plugin_id}"
                        }), websocket)
                    continue

                elif command == "GET_PLUGIN_SLOTS":
                    # Client requested plugin config (e.g. after reconnection)
                    # We need to read the config and send it back
                    plugin_config_path = os.path.join(os.getcwd(), "configs", "el_plugin_config.json")
                    if os.path.exists(plugin_config_path):
                        try:
                            with open(plugin_config_path, "r", encoding="utf-8") as f:
                                plugin_config = json.load(f)
                            
                            # Clean up nulls if needed, or just send
                            safe_config = {k: v for k, v in plugin_config.items() if v is not None}
                            
                            await manager.send_personal_message(json.dumps({
                                "command": "UPDATE_PLUGIN_SLOTS",
                                "data": safe_config
                            }), websocket)
                        except Exception as e:
                            if command_handler:
                                command_handler("error", f"Error reading plugin config: {e}")
                    continue

                elif command == "UPDATE_DOWNLOAD_FILE":
                    file_path = json_data.get("path")
                    # Security check: prevent directory traversal
                    if not file_path or ".." in file_path or file_path.startswith("/") or file_path.startswith("\\"):
                         await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": "Invalid file path"
                        }), websocket)
                         continue
                         
                    full_path = os.path.join(os.getcwd(), file_path)
                    
                    if os.path.exists(full_path) and os.path.isfile(full_path):
                        try:
                            with open(full_path, "rb") as f:
                                file_content = f.read()
                                encoded_content = base64.b64encode(file_content).decode('utf-8')
                                
                            await manager.send_personal_message(json.dumps({
                                "type": "UPDATE_RESPONSE_FILE",
                                "path": file_path,
                                "data": encoded_content
                            }), websocket)
                        except Exception as e:
                            await manager.send_personal_message(json.dumps({
                                "type": "error",
                                "message": f"Error reading file: {str(e)}"
                            }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            "type": "error",
                            "message": f"File not found: {file_path}"
                        }), websocket)
                    continue
                
                elif command == "CLIENT_SET_ACTIVE_SLOT":
                    # Client requested to switch active slot
                    slot_index = json_data.get("payload", {}).get("index")
                    
                    # Notify GUI (so server UI updates)
                    if command_handler:
                        command_handler("client_switched_slot", {"index": slot_index})
                    
                    # Broadcast to other clients (so everyone syncs)
                    await manager.broadcast(json.dumps({
                        "command": "SET_ACTIVE_SLOT",
                        "data": {"index": slot_index}
                    }))
                    continue

                # --- UPDATE LOGIC END ---
                
                # Передаем команду в обработчик (в GUI поток через callback, но тут осторожно с потоками)
                # Лучше передавать сырые данные, а GUI пусть разбирается
                if command_handler:
                    command_handler("command_received", json_data)
                
                # Отправляем подтверждение клиенту (опционально)
                # await manager.send_personal_message(f"Echo: {data}", websocket)
                
            except json.JSONDecodeError:
                if command_handler:
                    command_handler("error", f"Invalid JSON received: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        if command_handler:
            command_handler("client_disconnected", {"ip": websocket.client.host})
    except Exception as e:
        if command_handler:
            command_handler("error", f"WebSocket error: {str(e)}")
