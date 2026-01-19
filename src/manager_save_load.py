import json
import os
import base64

class ConfigManager:
    """
    Универсальный класс для сохранения и загрузки конфигурации JSON.
    Поддерживает простую обфускацию для чувствительных данных (паролей).
    """
    def __init__(self, file_path):
        self.file_path = file_path
        # Простой ключ для XOR-обфускации. 
        # ВНИМАНИЕ: Это не криптостойкая защита, а защита от "честного человека".
        self._xor_key = "BanditoSecretKey2026" 

    def save_config(self, data: dict):
        """
        Сохраняет словарь data в JSON файл.
        Автоматически создает директорию, если она не существует.
        """
        try:
            # Создаем директорию, если нужно
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True, "Config saved successfully"
        except Exception as e:
            return False, f"Error saving config: {e}"

    def load_config(self) -> dict:
        """
        Загружает данные из JSON файла.
        Возвращает словарь данных или пустой словарь, если файла нет или он поврежден.
        """
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading config {self.file_path}: {e}")
            return {}

    def encrypt_password(self, password: str) -> str:
        """
        Обфусцирует пароль: XOR + Base64.
        """
        if not password:
            return ""
        
        # XOR
        xor_result = []
        key_len = len(self._xor_key)
        for i, char in enumerate(password):
            key_char = self._xor_key[i % key_len]
            xor_result.append(chr(ord(char) ^ ord(key_char)))
        
        xor_str = "".join(xor_result)
        
        # Base64 Encode
        # encode to bytes -> b64encode -> decode back to utf-8 string
        encoded_bytes = base64.b64encode(xor_str.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Деобфусцирует пароль: Base64 Decode + XOR.
        """
        if not encrypted_password:
            return ""

        try:
            # Base64 Decode
            decoded_bytes = base64.b64decode(encrypted_password.encode('utf-8'))
            xor_str = decoded_bytes.decode('utf-8')

            # XOR (обратная операция такая же)
            original_result = []
            key_len = len(self._xor_key)
            for i, char in enumerate(xor_str):
                key_char = self._xor_key[i % key_len]
                original_result.append(chr(ord(char) ^ ord(key_char)))
            
            return "".join(original_result)
        except Exception as e:
            print(f"Decryption error: {e}")
            return ""
