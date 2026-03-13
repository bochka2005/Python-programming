import os
import file_manager

# Безопасный импорт библиотек
try:
    from pdf2docx import Converter
except ImportError:
    Converter = None

try:
    from docx2pdf import convert as convert_docx_lib
except ImportError:
    convert_docx_lib = None

def convert_pdf_to_docx(pdf_path):
    if Converter is None:
        return False, "Библиотека pdf2docx не установлена"
    
    if not os.path.exists(pdf_path):
        return False, f"Файл не найден: {pdf_path}"

    docx_path = os.path.splitext(pdf_path)[0] + ".docx"
    docx_path = file_manager.get_unique_filename(docx_path)

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        return True, docx_path
    except Exception as e:
        return False, str(e)

def convert_docx_to_pdf(docx_path):
    if convert_docx_lib is None:
        return False, "Библиотека docx2pdf не установлена"
    
    if os.name != 'nt':
        return False, "Конвертация DOCX->PDF работает только на Windows (требуется MS Word)"

    if not os.path.exists(docx_path):
        return False, f"Файл не найден: {docx_path}"

    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    pdf_path = file_manager.get_unique_filename(pdf_path)

    try:
        convert_docx_lib(docx_path, pdf_path)
        return True, pdf_path
    except Exception as e:
        return False, str(e)