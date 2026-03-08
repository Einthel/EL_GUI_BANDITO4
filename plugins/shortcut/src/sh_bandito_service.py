import os
import json
import base64
import shutil
import subprocess
from PySide6.QtCore import QSize

def load_json(path):
    """Универсальная загрузка JSON."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ShortcutService] Error loading JSON {path}: {e}")
        return {}

def save_json(path, data):
    """Универсальное сохранение JSON."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ShortcutService] Error saving JSON {path}: {e}")
        return False

def parse_style_to_css(style_data):
    """Преобразует JSON стилей в CSS строку."""
    css = ""
    for selector, props in style_data.items():
        props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
        css += f"{selector} {{ {props_str} }} \n"
    return css

def prepare_icon_payload(plugin_path, icon_rel_path):
    """Подготовка данных иконки для отправки (base64)."""
    full_path = os.path.join(plugin_path, icon_rel_path)
    if not os.path.exists(full_path):
        return None
    try:
        with open(full_path, "rb") as f:
            encoded_content = base64.b64encode(f.read()).decode('utf-8')
        return {
            "path": icon_rel_path,
            "content": encoded_content
        }
    except Exception as e:
        print(f"[ShortcutService] Icon prep error: {e}")
        return None

def execute_system_action(action):
    """Выполнение системного действия (программа или хоткей)."""
    act_type = action.get("type")
    value = action.get("value")
    if not value: return

    if act_type == "program":
        try:
            subprocess.Popen(value, shell=True)
        except Exception as e:
            print(f"[ShortcutService] Program exec error: {e}")
    elif act_type == "shortcut":
        try:
            import keyboard
            hotkey_str = value.lower().replace("win", "windows")
            keyboard.send(hotkey_str)
        except Exception as e:
            print(f"[ShortcutService] Hotkey error: {e}")

def copy_icon_to_plugin(src_path, plugin_path):
    """Копирует иконку в ресурсы плагина и возвращает относительный путь."""
    ico_dir = os.path.join(plugin_path, "resources", "ico")
    os.makedirs(ico_dir, exist_ok=True)
    
    file_name = os.path.basename(src_path)
    dest_path = os.path.join(ico_dir, file_name)
    
    try:
        if os.path.abspath(src_path) != os.path.abspath(dest_path):
            shutil.copy2(src_path, dest_path)
        return f"resources/ico/{file_name}"
    except Exception as e:
        print(f"[ShortcutService] Icon copy error: {e}")
        return None
