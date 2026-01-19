import uvicorn
from PySide6.QtCore import QThread, Signal
from server_main import app, set_command_handler

class ServerThread(QThread):
    """
    Поток для запуска FastAPI сервера через Uvicorn.
    Не блокирует основной GUI поток.
    """
    """
    Поток для запуска FastAPI сервера через Uvicorn.
    Не блокирует основной GUI поток.
    """
    # Сигнал для передачи логов/событий в GUI
    # msg_type: str (info, error, command), payload: dict/str
    server_signal = Signal(str, object)

    def __init__(self, host="0.0.0.0", port=8000):
        super().__init__()
        self.host = host
        self.port = int(port)
        self._is_running = True
        
        # Устанавливаем callback в server_main, чтобы получать события оттуда
        # Внимание: callback будет вызван из потока asyncio, а сигнал Qt потокобезопасен
        set_command_handler(self.handle_server_event)

    def handle_server_event(self, event_type, data):
        """Callback, вызываемый из FastAPI (server_main). Пересылает данные в GUI через сигнал."""
        self.server_signal.emit(event_type, data)

    def run(self):
        """Запуск сервера."""
        # uvicorn.run блокирует этот поток, пока сервер работает
        # log_level="warning" чтобы не спамить в консоль стандартными логами, мы будем слать свои
        try:
            self.server_signal.emit("info", f"Starting server on {self.host}:{self.port}")
            uvicorn.run(app, host=self.host, port=self.port, log_level="info")
        except Exception as e:
            self.server_signal.emit("error", f"Server failed to start: {e}")
        finally:
            self.server_signal.emit("info", "Server stopped")

    def stop(self):
        """
        Корректная остановка сервера.
        Uvicorn сложно остановить извне штатно без доступа к loop,
        но при завершении QThread и приложения он должен убиться.
        В будущем можно добавить механизм force shutdown через uvicorn.Server объект.
        """
        self.terminate() # Жесткая остановка потока (для простоты прототипа)
