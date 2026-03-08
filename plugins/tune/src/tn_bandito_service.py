import os
import json

class TuneClientoService:
    """Уровень I/O и данных для плагина Tune."""
    
    @staticmethod
    def load_json_config(file_path):
        """Загрузка JSON конфигурации."""
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def json_to_css(style_data):
        """Преобразование JSON-структуры стилей в CSS-строку."""
        css = ""
        for selector, props in style_data.items():
            props_str = "; ".join([f"{k}: {v}" for k, v in props.items()])
            css += f"{selector} {{ {props_str} }} \n"
        return css
