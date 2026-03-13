import os
import sys
import file_manager
import converter
import image_processor

# Пытаемся подключить красивый прогресс-бар, если есть
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable): return iterable

def change_dir_action():
    print(f"Текущий каталог: {file_manager.get_current_dir()}")
    path = input("Введите новый путь: ").strip()
    try:
        file_manager.change_directory(path)
        print("Каталог изменен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def convert_pdf_menu():
    files = file_manager.list_files(['.pdf'])
    if not files:
        print("PDF файлы не найдены.")
        return

    print("\n--- PDF файлы ---")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    
    choice = input("Номер файла (0 - все, -1 - назад): ")
    try:
        idx = int(choice)
    except ValueError:
        print("Введите число.")
        return

    if idx == -1: return

    # Выбираем файлы для обработки
    targets = []
    if idx == 0:
        targets = files
    elif 1 <= idx <= len(files):
        targets = [files[idx-1]]
    else:
        print("Неверный номер.")
        return

    for f in tqdm(targets):
        print(f"Конвертация {f}...")
        ok, res = converter.convert_pdf_to_docx(f)
        if ok: print(f"Успешно: {res}")
        else: print(f"Ошибка: {res}")

def convert_docx_menu():
    files = file_manager.list_files(['.docx'])
    if not files:
        print("DOCX файлы не найдены.")
        return

    print("\n--- DOCX файлы ---")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    
    choice = input("Номер файла (0 - все, -1 - назад): ")
    try:
        idx = int(choice)
    except ValueError:
        print("Введите число.")
        return
    
    if idx == -1: return

    targets = []
    if idx == 0:
        targets = files
    elif 1 <= idx <= len(files):
        targets = [files[idx-1]]
    else:
        return

    for f in tqdm(targets):
        print(f"Конвертация {f}...")
        ok, res = converter.convert_docx_to_pdf(f)
        if ok: print(f"Успешно: {res}")
        else: print(f"Ошибка: {res}")

def compress_img_menu():
    exts = ['.jpg', '.jpeg', '.png', '.gif']
    # Не показываем уже сжатые
    files = [f for f in file_manager.list_files(exts) if not f.startswith('compressed_')]
    
    if not files:
        print("Изображения не найдены.")
        return

    print("\n--- Изображения ---")
    for i, f in enumerate(files):
        size = os.path.getsize(f) / (1024*1024)
        print(f"{i+1}. {f} ({size:.2f} MB)")

    choice = input("Номер файла (0 - все, -1 - назад): ")
    try:
        idx = int(choice)
    except ValueError:
        print("Введите число.")
        return

    if idx == -1: return

    targets = []
    if idx == 0:
        targets = files
    elif 1 <= idx <= len(files):
        targets = [files[idx-1]]
    else:
        return

    try:
        qual = int(input("Качество (1-100): "))
        if not 1 <= qual <= 100: raise ValueError
    except:
        print("Неверное качество.")
        return

    saved_total = 0
    for f in tqdm(targets):
        orig_size = os.path.getsize(f)
        ok, res = image_processor.compress_image(f, qual)
        if ok:
            new_size = os.path.getsize(res)
            saved = orig_size - new_size
            saved_total += saved
            print(f"Сжато: {res}")
        else:
            print(f"Ошибка {f}: {res}")
    
    print(f"Всего сэкономлено: {saved_total / (1024*1024):.2f} MB")

def delete_files_menu():
    print("\n1. Начинается на...")
    print("2. Заканчивается на...")
    print("3. Содержит...")
    print("4. По расширению")
    mode = input("Выбор: ")
    
    files = file_manager.list_files()
    to_del = []
    
    pat = input("Введите текст/расширение: ")
    
    if mode == '1':
        to_del = [f for f in files if f.startswith(pat)]
    elif mode == '2':
        to_del = [f for f in files if f.endswith(pat)]
    elif mode == '3':
        to_del = [f for f in files if pat in f]
    elif mode == '4':
        if not pat.startswith('.'): pat = '.' + pat
        to_del = [f for f in files if f.lower().endswith(pat.lower())]
    else:
        return

    if not to_del:
        print("Файлы не найдены.")
        return

    print(f"Найдено файлов: {len(to_del)}")
    for f in to_del: print(f"- {f}")
    
    if input("Удалить? (Y/N): ").lower() == 'y':
        for f in to_del:
            file_manager.delete_file(f)
        print("Готово.")

def run_menu():
    while True:
        try:
            print(f"\n=== Office Tweaks v2.0 (Интерактивный) ===")
            print(f"Каталог: {os.getcwd()}")
            print("1. Сменить каталог")
            print("2. PDF -> DOCX")
            print("3. DOCX -> PDF")
            print("4. Сжать фото")
            print("5. Удалить файлы")
            print("0. Выход")
            
            choice = input("Ваш выбор: ")
            
            if choice == '1': change_dir_action()
            elif choice == '2': convert_pdf_menu()
            elif choice == '3': convert_docx_menu()
            elif choice == '4': compress_img_menu()
            elif choice == '5': delete_files_menu()
            elif choice == '0': break
            else: print("Неверный пункт.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка меню: {e}")