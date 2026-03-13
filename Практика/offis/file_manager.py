import os

def get_current_dir():
    return os.getcwd()

def change_directory(path):
    if not path:
        raise ValueError("Путь не может быть пустым.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Каталог не найден: {path}")
    os.chdir(path)

def list_files(extensions=None, directory=None):
    # Если directory не указана, ищем в текущей папке
    target_dir = directory if directory else os.getcwd()
    
    files = []
    try:
        for file in os.listdir(target_dir):
            full_path = os.path.join(target_dir, file)
            if os.path.isfile(full_path):
                if extensions:
                    for ext in extensions:
                        if file.lower().endswith(ext.lower()):
                            files.append(file) # Возвращаем имена файлов
                            break
                else:
                    files.append(file)
    except OSError:
        return []
    return sorted(files)

def get_unique_filename(filename):
    if not os.path.exists(filename):
        return filename
    
    base, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_name = f"{base}_({counter}){ext}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def delete_file(path):
    try:
        os.remove(path)
        return True, "Удалено"
    except Exception as e:
        return False, str(e)