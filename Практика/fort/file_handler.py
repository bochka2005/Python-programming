import os
import sys
import linecache
import random
from wheel_of_fortune.decorators import log_errors

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "wheel_of_fortune", relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

DATA_DIR = resource_path("data")
WORDS_FILE = resource_path("data/words.txt")
RECORD_FILE = resource_path("data/record.txt")

@log_errors
def random_word_generator():
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    used = set()

    while len(used) < total_lines:
        line_number = random.randint(1, total_lines)
        if line_number in used:
            continue
        used.add(line_number)
        word = linecache.getline(WORDS_FILE, line_number).strip()
        yield word

    linecache.clearcache()

@log_errors
def load_record() -> int:
    if not os.path.exists(RECORD_FILE):
        return 0
    try:
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            return int(f.read().strip() or 0)
    except:
        return 0

@log_errors
def save_record(record: int):
    with open(RECORD_FILE, 'w', encoding='utf-8') as f:
        f.write(str(record))
