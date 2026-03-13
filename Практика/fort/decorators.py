import time
from datetime import datetime

ERROR_LOG_FILE = "game.log"

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()            
        result = func(*args, **kwargs) 
        end = time.time()              
        total = int(end - start)      
        minutes, seconds = divmod(total, 60)

        print(f"\nВремя выполнения: {minutes} мин {seconds} сек")
        return result
    return wrapper


def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{now}] Ошибка в функции '{func.__name__}': {type(e).__name__}: {e}\n")
            
            print(f"\n⚠️ Произошла ошибка в {time.strftime('%H:%M:%S')}!")
            print(f"Ошибка: {type(e).__name__}: {e}")
            print(f"Подробности записаны в файл {ERROR_LOG_FILE}")
            
            raise   
    return wrapper


def log_game_event(message: str):
    """Простая функция для логирования игровых событий"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("game_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    
    return f"[{timestamp}] {message}"