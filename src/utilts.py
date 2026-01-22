import os
import sys

def get_base_path():
    """Возвращает путь к корню проекта."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
