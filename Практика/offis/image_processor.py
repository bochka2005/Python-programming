import os
import file_manager

try:
    from PIL import Image
except ImportError:
    Image = None

def compress_image(img_path, quality):
    if Image is None:
        return False, "Библиотека Pillow не установлена"
    
    if not os.path.exists(img_path):
        return False, f"Файл не найден: {img_path}"

    try:
        # Формируем имя файла
        dir_name = os.path.dirname(img_path)
        file_name = os.path.basename(img_path)
        new_name = "compressed_" + file_name
        full_new_path = os.path.join(dir_name, new_name)
        
        final_path = file_manager.get_unique_filename(full_new_path)

        with Image.open(img_path) as img:
            # Особенность PNG (нужно уменьшать цвета, чтобы сжать)
            if img_path.lower().endswith('.png') and quality < 100:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                img.save(final_path, optimize=True)
            elif img_path.lower().endswith('.jpg') or img_path.lower().endswith('.jpeg'):
                img.save(final_path, quality=quality, optimize=True)
            else:
                img.save(final_path, optimize=True)
        
        return True, final_path
    except Exception as e:
        return False, str(e)