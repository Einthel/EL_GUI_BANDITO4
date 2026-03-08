import os
import json
import base64

def load_config(plugin_path):
    """Загружает конфигурацию кнопок из JSON."""
    config_path = os.path.join(plugin_path, "config", "button_shortcut.json")
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {}

def save_config(plugin_path, data):
    """Сохраняет конфигурацию кнопок в JSON."""
    config_path = os.path.join(plugin_path, "config", "button_shortcut.json")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        return False

def load_style_data(plugin_path):
    """Загружает сырые данные стилей из JSON."""
    style_path = os.path.join(plugin_path, "config", "style_shortcut_cliento.json")
    if os.path.exists(style_path):
        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            pass
    return {}

def parse_style_to_css(style_data):
    """Преобразует JSON стилей в CSS строку."""
    css = ""
    for selector, props in style_data.items():
        if selector == "animation": continue
        props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
        css += f"{selector} {{ {props_str} }} \n"
    return css

def load_anim_config(plugin_path):
    """Извлекает настройки анимации из конфига стилей."""
    style_data = load_style_data(plugin_path)
    return style_data.get("animation", {
        "duration": 100, 
        "scale_factor": 0.95, 
        "easing_curve": "OutQuad"
    })

def handle_icon_save(plugin_path, icon_data):
    """Декодирует base64 и сохраняет иконку."""
    rel_path = icon_data.get("path")
    content_b64 = icon_data.get("content")
    
    if not rel_path or not content_b64:
        return None
        
    full_path = os.path.join(plugin_path, rel_path)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        file_data = base64.b64decode(content_b64)
        with open(full_path, "wb") as f:
            f.write(file_data)
        return full_path
    except Exception as e:
        return None
