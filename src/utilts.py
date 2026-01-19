import os
import sys
import subprocess

def compile_ui_files(ui_dir, output_dir):
    """
    Рекурсивно находит и компилирует все .ui файлы в .py,
    из директории ui_dir в директорию output_dir.
    Файлы с 'bandito' в имени попадают в output_dir/ui_bandito.
    Файлы с 'cliento' в имени попадают в output_dir/ui_cliento.
    Перекомпилирует, только если .py файл отсутствует или .ui файл новее.
    """
    if not os.path.isdir(ui_dir):
        print(f"ОШИБКА: Директория с UI-файлами не найдена: {ui_dir}")
        return
    
    # Создаем базовый output_dir, если его нет
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
            
            # Определяем подпапку назначения на основе имени файла
            if "bandito" in ui_file:
                target_subdir = os.path.join(output_dir, "ui_bandito")
            elif "cliento" in ui_file:
                target_subdir = os.path.join(output_dir, "ui_cliento")
            else:
                target_subdir = output_dir

            # Создаем подпапку, если её нет
            if not os.path.exists(target_subdir):
                try:
                    os.makedirs(target_subdir)
                except OSError as e:
                    print(f"ОШИБКА: Не удалось создать поддиректорию {target_subdir}: {e}")
                    continue

            # Generate the name for the .py file (e.g., widget.ui -> ui_widget.py)
            base_name = os.path.splitext(ui_file)[0]
            py_file_name = f"ui_{base_name}.py"
            py_path = os.path.join(target_subdir, py_file_name)

            # Recompile if .py file is missing or .ui is newer
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
                    # Using check=True to raise an exception on error
                    subprocess.run(
                        ['pyside6-uic', ui_path, '-o', py_path], 
                        check=True,
                        capture_output=True, # Hide verbose output unless there's an error
                        text=True
                    )
                    print("Компиляция прошла успешно.")
                except FileNotFoundError:
                    print("\n" + "="*50)
                    print("ОШИБКА: Команда 'pyside6-uic' не найдена.")
                    print("Пожалуйста, убедитесь, что 'pyside6-tools' установлен.")
                    print("Вы можете установить его командой: pip install pyside6-tools")
                    print("="*50)
                    # Не выходим жестко, чтобы программа могла попытаться работать дальше (хотя скорее всего упадет при импорте)
                except subprocess.CalledProcessError as e:
                    print(f"\n" + "="*50)
                    print(f"ОШИБКА: Не удалось скомпилировать '{ui_path}'.")
                    print(f"Детали:\n{e.stderr}")
                    print("="*50)
