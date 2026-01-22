import os
import subprocess

def _compile_if_needed(ui_path, py_path):
    """
    Внутренняя функция: компилирует .ui в .py, если .py отсутствует или .ui новее.
    Возвращает True, если компиляция была произведена, иначе False.
    """
    recompile = False
    if not os.path.exists(py_path):
        recompile = True
        print(f"Файл '{py_path}' не найден. Требуется компиляция.")
    elif os.path.getmtime(ui_path) > os.path.getmtime(py_path):
        recompile = True
        print(f"Изменения в '{ui_path}'. Требуется перекомпиляция.")

    if recompile:
        print(f"Компиляция '{ui_path}' -> '{py_path}'...")
        try:
            subprocess.run(
                ['pyside6-uic', ui_path, '-o', py_path], 
                check=True,
                capture_output=True,
                text=True
            )
            print("Компиляция прошла успешно.")
            return True
        except FileNotFoundError:
            print("\n" + "="*50)
            print("ОШИБКА: Команда 'pyside6-uic' не найдена.")
            print("Пожалуйста, убедитесь, что 'pyside6-tools' установлен (pip install pyside6-tools).")
            print("="*50)
        except subprocess.CalledProcessError as e:
            print(f"\n" + "="*50)
            print(f"ОШИБКА: Не удалось скомпилировать '{ui_path}'.")
            print(f"Детали:\n{e.stderr}")
            print("="*50)
    
    return False

def compile_ui_files(ui_dir, output_dir):
    """
    Основной компилятор: находит .ui файлы в ui_dir, 
    распределяет их по подпапкам (ui_bandito/ui_cliento) в output_dir 
    и компилирует.
    """
    if not os.path.isdir(ui_dir):
        print(f"ОШИБКА: Директория с UI-файлами не найдена: {ui_dir}")
        return
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Создана директория для скомпилированных файлов: {output_dir}")
        except OSError as e:
            print(f"ОШИБКА: Не удалось создать директорию {output_dir}: {e}")
            return

    for root, _, files in os.walk(ui_dir):
        for ui_file in files:
            if not ui_file.endswith(".ui"):
                continue

            ui_path = os.path.join(root, ui_file)
            
            # Логика распределения по папкам (сохранена из старого utilts.py)
            if "bandito" in ui_file:
                target_subdir = os.path.join(output_dir, "ui_bandito")
            elif "cliento" in ui_file:
                target_subdir = os.path.join(output_dir, "ui_cliento")
            else:
                target_subdir = output_dir

            if not os.path.exists(target_subdir):
                try:
                    os.makedirs(target_subdir)
                except OSError as e:
                    print(f"ОШИБКА: Не удалось создать поддиректорию {target_subdir}: {e}")
                    continue

            base_name = os.path.splitext(ui_file)[0]
            py_file_name = f"ui_{base_name}.py"
            py_path = os.path.join(target_subdir, py_file_name)

            _compile_if_needed(ui_path, py_path)

def compile_plugin_ui_files(plugins_dir):
    """
    Компилятор плагинов: находит .ui файлы внутри папки плагинов
    и компилирует их "In-Place" (рядом с исходником), добавляя префикс ui_.
    """
    if not os.path.isdir(plugins_dir):
        # Если папки плагинов нет - это не критическая ошибка, просто нечего компилировать
        # print(f"Директория плагинов не найдена: {plugins_dir}") 
        return

    print(f"Проверка UI файлов плагинов в '{plugins_dir}'...")
    
    for root, _, files in os.walk(plugins_dir):
        for ui_file in files:
            if not ui_file.endswith(".ui"):
                continue

            ui_path = os.path.join(root, ui_file)
            
            # Формируем имя целевого файла: shortcut.ui -> ui_shortcut.py
            base_name = os.path.splitext(ui_file)[0]
            py_file_name = f"ui_{base_name}.py"
            
            # Целевой путь - ТАМ ЖЕ, где и ui файл
            py_path = os.path.join(root, py_file_name)

            _compile_if_needed(ui_path, py_path)
