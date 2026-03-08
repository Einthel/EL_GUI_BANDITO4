import sys
import os
import json
import urllib.request
from PySide6.QtCore import QObject, Signal

# Попытка импорта ServerThread
# Так как el_core может использоваться в разных контекстах, пробуем разные пути
try:
    # Если запущен из el_bandito.py, путь к el_bandito уже в sys.path
    from server_thread import ServerThread
except ImportError:
    try:
        # Если запущен из корня проекта
        from el_bandito.server_thread import ServerThread
    except ImportError:
        ServerThread = None
        print("[ElComManager] Warning: ServerThread class not found. Server functionality will be disabled.")

class ElComManager(QObject):
    """
    Менеджер коммуникаций (Network Layer).
    Обертка над ServerThread (FastAPI) для удобного взаимодействия с Core.
    Изолирует сетевую логику от бизнес-логики.
    """
    
    # --- Сигналы для Core ---
    client_connected = Signal(dict)      # {ip: ...}
    client_disconnected = Signal(dict)   # {ip: ...}
    command_received = Signal(dict)      # Полный JSON от клиента
    client_switched_slot = Signal(int)   # Индекс слота, выбранного клиентом
    log_message = Signal(str, str)       # type (info/error), message

    def __init__(self, port=8000):
        super().__init__()
        self.port = port
        self.server_thread = None

    def start_service(self):
        """Запускает WebSocket сервер в отдельном потоке."""
        if self.server_thread:
            self.log_message.emit("warning", "Server already running")
            return

        if not ServerThread:
            self.log_message.emit("error", "ServerThread class not available")
            return

        self.server_thread = ServerThread(port=self.port)
        self.server_thread.server_signal.connect(self._handle_server_signal)
        self.server_thread.start()
        self.log_message.emit("info", f"Service started on port {self.port}")

    def stop_service(self):
        """Останавливает сервер."""
        if self.server_thread:
            self.server_thread.stop()
            self.server_thread.wait()
            self.server_thread = None
            self.log_message.emit("info", "Service stopped")

    def broadcast(self, command: str, data: dict = None):
        """
        Отправляет сообщение всем подключенным клиентам.
        Использует локальный API endpoint FastAPI сервера для thread-safe рассылки.
        """
        try:
            url = f"http://127.0.0.1:{self.port}/api/broadcast"
            payload = {
                "command": command,
                "data": data if data is not None else {}
            }
            json_payload = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(url, data=json_payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    self.log_message.emit("error", f"Broadcast failed with status {response.status}")
        except Exception as e:
            # Часто возникает при остановке сервера, можно игнорировать или логировать как debug
            self.log_message.emit("error", f"Broadcast failed: {e}")

    def _handle_server_signal(self, type_msg, data):
        """
        Обработка сигналов от ServerThread и перенаправление в Core.
        Преобразует сырые данные в типизированные сигналы.
        """
        # Логирование
        if type_msg in ["info", "error", "warning"]:
            self.log_message.emit(type_msg, str(data))
        
        # События подключения
        elif type_msg == "client_connected":
            payload = data if isinstance(data, dict) else {"ip": str(data)}
            self.client_connected.emit(payload)
        
        elif type_msg == "client_disconnected":
            payload = data if isinstance(data, dict) else {"ip": str(data)}
            self.client_disconnected.emit(payload)
        
        # Команды от клиента
        elif type_msg == "command_received":
            self.command_received.emit(data)
        
        # Специфичные события (переключение слота клиентом)
        elif type_msg == "client_switched_slot":
            index = data.get("index")
            if index is not None:
                try:
                    self.client_switched_slot.emit(int(index))
                except ValueError:
                    pass
