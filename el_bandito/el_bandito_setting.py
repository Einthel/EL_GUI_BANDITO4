import sys
import os
import socket
import subprocess
import platform

from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox, QApplication
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QIntValidator

# Для корректного импорта, если запускаем файл напрямую (для теста)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Импорт менеджера конфигурации
from src.manager_save_load import ConfigManager

# Импорт UI (обернут в try для безопасности IDE, хотя в рантайме файлы должны быть)
try:
    from resources.ui_done.ui_bandito.ui_bandito_settings import Ui_Setting_bandito_widget
except ImportError:
    # Заглушка, если UI еще не скомпилирован
    Ui_Setting_bandito_widget = object

class BanditoSettings(QWidget):
    def __init__(self):
        super(BanditoSettings, self).__init__()
        self.ui = Ui_Setting_bandito_widget()
        self.ui.setupUi(self)
        
        # Модальное окно (блокирует родителя)
        self.setWindowModality(Qt.ApplicationModal)

        # Config Manager
        config_path = os.path.join(project_root, "configs", "el_bandito_config.json")
        self.config_manager = ConfigManager(config_path)

        # 1. IP Source (Manual Entry)
        self.ui.ip_source_lineE.setReadOnly(False)
        self.ui.ip_source_lineE.setPlaceholderText("192.168.0.X")

        # 2. Validators
        self.setup_validators()

        # 3. Password Logic
        self.ui.pass_lineE.setEchoMode(QLineEdit.Password)
        self.ui.show_pass_checkB.toggled.connect(self.toggle_password_visibility)

        # 4. Buttons Connections
        self.ui.connect_toolB.clicked.connect(self.on_connect)
        self.ui.disconnect_toolB.clicked.connect(self.on_disconnect)
        self.ui.save_toolB.clicked.connect(self.on_save)
        self.ui.ping_toolB.clicked.connect(self.on_ping)

        # 5. Load Settings
        self.load_settings_to_ui()

    def setup_validators(self):
        """Настройка валидаторов для полей ввода."""
        
        # --- IP Validator (Destination & Source) ---
        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ip_regex = QRegularExpression(f"^{ip_range}\\.{ip_range}\\.{ip_range}\\.{ip_range}$")
        
        ip_validator_dest = QRegularExpressionValidator(ip_regex, self)
        self.ui.ip_destination_lineE.setValidator(ip_validator_dest)
        self.ui.ip_destination_lineE.setPlaceholderText("192.168.1.100")
        
        ip_validator_source = QRegularExpressionValidator(ip_regex, self)
        self.ui.ip_source_lineE.setValidator(ip_validator_source)

        # --- Port Validator ---
        port_validator = QIntValidator(0, 65535, self)
        self.ui.port_lineE.setValidator(port_validator)
        self.ui.port_lineE.setPlaceholderText("8000")

        # --- Login Validator ---
        login_regex = QRegularExpression(r"^\S+$")
        login_validator = QRegularExpressionValidator(login_regex, self)
        self.ui.login_lineE.setValidator(login_validator)

    def toggle_password_visibility(self, checked):
        """Переключает видимость пароля."""
        if checked:
            self.ui.pass_lineE.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.pass_lineE.setEchoMode(QLineEdit.Password)

    def load_settings_to_ui(self):
        """Загружает настройки из JSON в UI."""
        data = self.config_manager.load_config()
        if not data:
            return 

        if "ip_destination" in data:
            self.ui.ip_destination_lineE.setText(data["ip_destination"])
        if "port" in data:
            self.ui.port_lineE.setText(str(data["port"]))
        if "login" in data:
            self.ui.login_lineE.setText(data["login"])
        if "ip_source" in data:
            self.ui.ip_source_lineE.setText(data["ip_source"])
        elif "last_ip_source" in data:
            self.ui.ip_source_lineE.setText(data["last_ip_source"])
        
        if "password_encrypted" in data:
            decrypted_pass = self.config_manager.decrypt_password(data["password_encrypted"])
            self.ui.pass_lineE.setText(decrypted_pass)

    def on_save(self):
        """Собирает данные из UI и сохраняет в JSON."""
        data = {
            "ip_source": self.ui.ip_source_lineE.text(),
            "ip_destination": self.ui.ip_destination_lineE.text(),
            "port": self.ui.port_lineE.text(),
            "login": self.ui.login_lineE.text(),
            "password_encrypted": self.config_manager.encrypt_password(self.ui.pass_lineE.text())
        }

        success, msg = self.config_manager.save_config(data)
        if success:
            self.log_status("Settings saved successfully")
            QMessageBox.information(self, "Success", "Settings saved!")
        else:
            self.log_status(f"Save error: {msg}")
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{msg}")

    def on_connect(self):
        print("Connect clicked")
        self.log_status("Connecting...")

    def on_disconnect(self):
        print("Disconnect clicked")
        self.log_status("Disconnected")

    def on_ping(self):
        """Пингует IP из поля назначения (4 пакета, стандартный размер)."""
        target_ip = self.ui.ip_destination_lineE.text()
        if not target_ip:
            self.log_status("Error: No IP to ping")
            return

        self.log_status(f"Pinging {target_ip} (4 packets)...")
        QApplication.processEvents() # Обновляем UI перед началом блокирующей операции
        
        # Определяем параметры для Windows
        if platform.system().lower() == 'windows':
            count_flag = '-n'
            # Размер буфера 32 байта (стандарт Windows)
            size_flag = '-l' 
            size_val = '32'
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            count_flag = '-c'
            # В Linux размер данных задается -s. 32 байта данных + 28 байт заголовка = 60 байт (как в Windows по умолчанию 32 байта payload)
            size_flag = '-s' 
            size_val = '32'
            
            startupinfo = None
            creationflags = 0

        # Команда ping: ping -n 4 -l 32 <ip>
        command = ['ping', count_flag, '4', size_flag, size_val, target_ip]

        try:
            # Запускаем процесс
            # Убрали timeout, чтобы дождаться завершения команды
            result = subprocess.run(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                # timeout=15, 
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            # Декодируем вывод (cp866 для русской Windows консоли)
            try:
                output = result.stdout.decode('cp866')
            except:
                output = result.stdout.decode('utf-8', errors='ignore')

            if result.returncode == 0:
                # Если успешно, пробуем найти строку со средним временем или потерями
                # Пример: "Minimum = 32ms, Maximum = 32ms, Average = 32ms"
                lines = [l.strip() for l in output.split('\n') if l.strip()]
                status_msg = f"Ping {target_ip}: OK"
                for line in lines:
                     if "Average" in line or "Среднее" in line: # En/Ru
                         status_msg = f"OK. {line}"
                         break
                self.log_status(status_msg)
            else:
                # Если ошибка, ищем описание ошибки
                lines = [l.strip() for l in output.split('\n') if l.strip()]
                error_msg = f"Ping {target_ip}: FAILED"
                for line in lines:
                    # Ищем типичные ошибки
                    if any(x in line for x in ["unreachable", "timed out", "недоступен", "превышен", "General failure", "Общий сбой"]):
                        error_msg = line
                        break
                self.log_status(error_msg)

        except Exception as e:
            self.log_status(f"Ping error: {str(e)}")

    def log_status(self, message):
        """Выводит сообщения в статусную строку (status_lineE)"""
        self.ui.status_lineE.setText(message)

# Для автономного тестирования этого файла
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BanditoSettings()
    window.show()
    sys.exit(app.exec())
