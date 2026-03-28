import json
from PySide6.QtCore import QObject, Signal, QUrl, QTimer
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtNetwork import QAbstractSocket

class BanditoClient(QObject):
    """
    WebSocket клиент для связи с сервером Bandito.
    Работает асинхронно через сигналы Qt.
    """
    # Сигналы для UI
    connected = Signal()
    disconnected = Signal()
    message_received = Signal(dict) # Передает распаршенный JSON
    log_message = Signal(str) # Для вывода логов в консоль/UI

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = QWebSocket()
        self.url = QUrl()
        
        # Таймер для авто-переподключения
        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setInterval(3000) # 3 секунды
        self.reconnect_timer.timeout.connect(self.connect_to_server)

        # Подключаем сигналы сокета
        self.client.connected.connect(self._on_connected)
        self.client.disconnected.connect(self._on_disconnected)
        self.client.textMessageReceived.connect(self._on_message_received)
        self.client.errorOccurred.connect(self._on_error)

    def set_connection_info(self, ip, port):
        """Устанавливает параметры подключения."""
        # Формат: ws://192.168.1.100:8000/ws
        address = f"ws://{ip}:{port}/ws"
        self.url = QUrl(address)

    def connect_to_server(self):
        """Попытка подключения."""
        # QWebSocket.state() возвращает enum QAbstractSocket.SocketState
        if self.client.state() == QAbstractSocket.UnconnectedState:
            self.log_message.emit(f"Connecting to {self.url.toString()}...")
            self.client.open(self.url)

    def disconnect_from_server(self):
        """Принудительное отключение."""
        self.reconnect_timer.stop()
        self.client.close()

    def send_command(self, command: str, payload: dict = None):
        """Отправка JSON команды на сервер."""
        if self.client.state() == QAbstractSocket.ConnectedState:
            msg = {
                "command": command,
                "payload": payload or {}
            }
            try:
                json_str = json.dumps(msg)
                self.client.sendTextMessage(json_str)
                self.log_message.emit(f"Sent: {command}")
            except Exception as e:
                self.log_message.emit(f"Send error: {e}")
        else:
            self.log_message.emit("Error: Not connected")

    # --- Внутренние обработчики ---

    def _on_connected(self):
        self.log_message.emit("Connected!")
        self.reconnect_timer.stop()
        self.connected.emit()
        # Request initial state
        self.send_command("GET_PLUGIN_SLOTS")

    def _on_disconnected(self):
        self.log_message.emit("Disconnected.")
        self.disconnected.emit()
        # Запускаем таймер переподключения, если не было ручного стопа
        # (в простой реализации всегда пробуем реконнект)
        if not self.reconnect_timer.isActive():
            self.reconnect_timer.start()

    def _on_message_received(self, message):
        """Обработка входящих сообщений от сервера."""
        try:
            data = json.loads(message)
            self.message_received.emit(data)
            
            # Логирование с защитой от больших бинарных данных
            log_data = data.copy()
            command = data.get("command", "")
            
            # Если это обновление файла, не выводим content/data
            if command == "SHORTCUT_ICON_UPDATE" and "data" in log_data:
                # Создаем копию вложенного словаря, чтобы не испортить оригинал
                log_data["data"] = log_data["data"].copy()
                if "content" in log_data["data"]:
                    path = log_data["data"].get("path", "unknown")
                    log_data["data"]["content"] = f"<Binary Data for {path}>"
            
            # Общая защита от длинных строк (на случай других команд)
            msg_str = str(log_data)
            if len(msg_str) > 500:
                msg_str = msg_str[:500] + "... [truncated]"
                
            self.log_message.emit(f"Received: {msg_str}")
            
        except json.JSONDecodeError:
            self.log_message.emit(f"Received raw: {message[:100]}...")

    def _on_error(self, error_code):
        error_msg = self.client.errorString()
        self.log_message.emit(f"Socket Error: {error_msg}")
