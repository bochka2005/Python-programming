import argparse
import sys
import os
import file_manager
import converter
import image_processor

def run_cli_mode():
    parser = argparse.ArgumentParser(description="Office Tweaks CLI Tool")

    # Взаимоисключающие группы команд
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pdf2docx', help='Путь к PDF файлу или "all"')
    group.add_argument('--docx2pdf', help='Путь к DOCX файлу или "all"')
    group.add_argument('--compress-images', help='Путь к картинке или "all"')
    group.add_argument('--delete', action='store_true', help='Режим удаления')

    # Доп. параметры
    parser.add_argument('--workdir', help='Рабочая папка')
    parser.add_argument('--quality', type=int, help='Качество сжатия (1-100)')
    
    # Параметры удаления
    parser.add_argument('--delete-mode', choices=['startswith', 'endswith', 'contains', 'extension'])
    parser.add_argument('--delete-pattern', help='Шаблон для удаления')
    parser.add_argument('--delete-dir', help='Папка для очистки')
    
    # Флаг для принудительного меню
    parser.add_argument('-i', '--interactive', action='store_true', help='Запустить меню')

    args = parser.parse_args()

    # Если есть флаг -i, говорим главному модулю запустить меню
    if args.interactive:
        return False

    # Если не выбрана ни одна команда, тоже в меню
    if not (args.pdf2docx or args.docx2pdf or args.compress_images or args.delete):
        return False

    # 1. Установка рабочей папки
    current_workdir = os.getcwd()
    if args.workdir:
        try:
            file_manager.change_directory(args.workdir)
            current_workdir = args.workdir
            print(f"Рабочий каталог установлен: {current_workdir}")
        except Exception as e:
            print(f"Ошибка смены каталога: {e}")
            sys.exit(1)

    # 2. Логика PDF -> DOCX
    if args.pdf2docx:
        target = args.pdf2docx
        files_to_process = []
        
        if target == 'all':
            files_to_process = file_manager.list_files(['.pdf'])
        elif os.path.exists(target):
            files_to_process = [target]
        else:
            print(f"Файл не найден: {target}")
            sys.exit(1)
            
        print(f"Обработка {len(files_to_process)} файлов...")
        for f in files_to_process:
            ok, msg = converter.convert_pdf_to_docx(f)
            print(f"{f}: {'OK' if ok else 'FAIL'} -> {msg}")

    # 3. Логика DOCX -> PDF
    elif args.docx2pdf:
        target = args.docx2pdf
        files_to_process = []
        
        if target == 'all':
            files_to_process = file_manager.list_files(['.docx'])
        elif os.path.exists(target):
            files_to_process = [target]
        else:
            print(f"Файл не найден: {target}")
            sys.exit(1)
            
        print(f"Обработка {len(files_to_process)} файлов...")
        for f in files_to_process:
            ok, msg = converter.convert_docx_to_pdf(f)
            print(f"{f}: {'OK' if ok else 'FAIL'} -> {msg}")

    # 4. Логика сжатия изображений
    elif args.compress_images:
        if not args.quality:
            print("Ошибка: Не указано --quality (1-100)")
            sys.exit(1)
        
        if not 1 <= args.quality <= 100:
            print("Ошибка: Quality должно быть от 1 до 100")
            sys.exit(1)

        target = args.compress_images
        exts = ['.jpg', '.jpeg', '.png', '.gif']
        files_to_process = []

        if target == 'all':
            # Ищем файлы в текущем каталоге (или workdir), исключая сжатые
            all_imgs = file_manager.list_files(exts)
            files_to_process = [f for f in all_imgs if not f.startswith('compressed_')]
        elif os.path.exists(target):
            files_to_process = [target]
        else:
            print(f"Файл не найден: {target}")
            sys.exit(1)

        print(f"Сжатие {len(files_to_process)} изображений (Quality: {args.quality})...")
        for f in files_to_process:
            ok, msg = image_processor.compress_image(f, args.quality)
            print(f"{f}: {'OK' if ok else 'FAIL'} -> {msg}")

    # 5. Логика удаления
    elif args.delete:
        if not args.delete_mode or not args.delete_pattern:
            print("Ошибка: укажите --delete-mode и --delete-pattern")
            sys.exit(1)

        # Если указан delete-dir, используем его, иначе текущий
        del_dir = args.delete_dir if args.delete_dir else current_workdir
        if not os.path.exists(del_dir):
            print(f"Папка не найдена: {del_dir}")
            sys.exit(1)

        files = file_manager.list_files(directory=del_dir)
        to_delete = []
        pat = args.delete_pattern

        if args.delete_mode == 'startswith':
            to_delete = [f for f in files if f.startswith(pat)]
        elif args.delete_mode == 'endswith':
            to_delete = [f for f in files if f.endswith(pat)]
        elif args.delete_mode == 'contains':
            to_delete = [f for f in files if pat in f]
        elif args.delete_mode == 'extension':
            if not pat.startswith('.'): pat = '.' + pat
            to_delete = [f for f in files if f.lower().endswith(pat.lower())]

        if not to_delete:
            print("Файлы для удаления не найдены.")
        else:
            print(f"Удаление {len(to_delete)} файлов из {del_dir}...")
            for f in to_delete:
                full_path = os.path.join(del_dir, f)
                ok, msg = file_manager.delete_file(full_path)
                print(f"{f}: {msg}")

    return True # Возвращаем True, если отработали в CLI