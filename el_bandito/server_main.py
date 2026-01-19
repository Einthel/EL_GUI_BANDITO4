import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

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

# Создаем приложение FastAPI
app = FastAPI()

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
