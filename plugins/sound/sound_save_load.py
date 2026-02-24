import os
import json
import threading

# Глобальная блокировка и кэш
_config_lock = threading.Lock()
_config_cache = {}
_last_mtime = 0

def load_sound_config(plugin_path):
    """Загружает конфигурацию с использованием кэша."""
    global _config_cache, _last_mtime
    config_path = os.path.join(plugin_path, "config", "config_sound.json")
    
    if not os.path.exists(config_path):
        return {}

    try:
        current_mtime = os.path.getmtime(config_path)
        with _config_lock:
            # Если кэш пуст или файл на диске новее, читаем с диска
            if not _config_cache or current_mtime > _last_mtime:
                with open(config_path, 'r', encoding='utf-8') as f:
                    _config_cache = json.load(f)
                    _last_mtime = current_mtime
            
            return _config_cache.copy()
    except Exception as e:
        print(f"[SoundSaveLoad] Error loading config: {e}")
        return _config_cache.copy() if _config_cache else {}

def save_sound_config(plugin_path, config_data):
    """Сохраняет конфигурацию и обновляет кэш."""
    global _config_cache, _last_mtime
    config_path = os.path.join(plugin_path, "config", "config_sound.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with _config_lock:
        try:
            # 1. Сначала гарантируем, что у нас актуальный кэш с диска
            if os.path.exists(config_path):
                current_mtime = os.path.getmtime(config_path)
                if not _config_cache or current_mtime > _last_mtime:
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            _config_cache = json.load(f)
                            _last_mtime = current_mtime
                    except:
                        pass

            # 2. Объединяем данные
            new_config = _config_cache.copy() if _config_cache else {}
            new_config.update(config_data)
            
            # 3. Если после объединения ничего не изменилось, выходим
            if new_config == _config_cache and os.path.exists(config_path):
                return True

            # 4. Записываем на диск
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            
            # 5. Обновляем кэш и время
            _config_cache = new_config
            _last_mtime = os.path.getmtime(config_path)
            return True
        except Exception as e:
            print(f"[SoundSaveLoad] Error saving config: {e}")
            return False

def update_selected_device(plugin_path, device_name):
    """Обновляет только выбранное устройство."""
    return save_sound_config(plugin_path, {"selected_device": device_name})
