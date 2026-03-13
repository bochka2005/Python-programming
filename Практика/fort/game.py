from wheel_of_fortune.file_handler import random_word_generator, load_record, save_record
from wheel_of_fortune.decorators import timer, log_errors, log_game_event
from wheel_of_fortune.utils import mask_word, choose_lives
import time
import sys


@timer
@log_errors
def start_game():
    log_game_event("=== НАЧАЛО ИГРЫ ===")
    
    while True:
        print("=== ПОЛЕ ЧУДЕС ===")
        best_record = load_record()
        print(f"🏆 Ваш лучший рекорд: {best_record} слов")
        log_game_event(f"Загружен рекорд: {best_record} слов")

        while True:
            try:
                level = int(input(
                    "\nВыберите уровень сложности:\n"
                    "1. Легкий (7 жизней)\n"
                    "2. Средний (5 жизней)\n"
                    "3. Сложный (3 жизни)\nВаш выбор: "
                ))
                if level not in (1, 2, 3):
                    raise ValueError
                log_game_event(f"Выбран уровень сложности: {level}")
                break
            except ValueError as e:
                log_game_event(f"Ошибка ввода уровня: {e}")
                print("Некорректный ввод! Введите 1, 2 или 3.")

        generator = random_word_generator()
        guessed_words = 0
        start_time = time.time()
        game_over = False

        for index, word in enumerate(generator, 1):
            lives = choose_lives(level)
            guessed_letters = []
            
            log_game_event(f"Слово #{index}: '{word}', жизней: {lives}")

            print(f"\nСлово №{index}")
            print(mask_word(word, guessed_letters))
            print(f"Количество жизней: {'♥' * lives}")

            while lives > 0:
                user_input = input("\nНазовите букву или слово целиком: ").strip().lower()
                log_game_event(f"Игрок ввел: '{user_input}'")

                if not user_input.isalpha():
                    log_game_event(f"Некорректный ввод: '{user_input}'")
                    print("Ошибка: можно вводить только буквы!")
                    print(f"Количество жизней: {'♥' * lives}")
                    continue

                if len(user_input) > 1:
                    if user_input == word:
                        log_game_event(f"Угадано слово целиком: '{word}'")
                        print(f"Слово отгадано: {word}")
                        guessed_words += 1
                        log_game_event(f"Всего угадано слов: {guessed_words}")
                        print(f"Количество жизней: {'♥' * lives}")
                        break
                    else:
                        log_game_event(f"Неверное слово: '{user_input}', правильное: '{word}'")
                        print("Неверное слово! Вы проиграли.")
                        lives = 0
                        break

                letter = user_input

                if letter in guessed_letters:
                    lives -= 1
                    log_game_event(f"Повтор буквы '{letter}', осталось жизней: {lives}")
                    print(f"Буква '{letter}' уже была! Осталось жизней: {'♥' * lives}")
                    continue

                if letter in word:
                    guessed_letters.append(letter)
                    log_game_event(f"Правильная буква '{letter}'")
                    print(mask_word(word, guessed_letters))
                    print(f"Количество жизней: {'♥' * lives}")

                    if all(l in guessed_letters for l in set(word)):
                        log_game_event(f"Слово полностью угадано: '{word}'")
                        print(f"Слово отгадано: {word}")
                        guessed_words += 1
                        log_game_event(f"Всего угадано слов: {guessed_words}")
                        print(f"Количество жизней: {'♥' * lives}")
                        break
                else:
                    lives -= 1
                    log_game_event(f"Неправильная буква '{letter}', осталось жизней: {lives}")
                    print(f"Буквы '{letter}' нет в слове!")
                    print(f"Количество жизней: {'♥' * lives}")
            
            if lives == 0:
                log_game_event(f"Жизни закончились. Слово было: '{word}'")
                print("\n💔 ИГРА ОКОНЧЕНА! 💔")
                print("К сожалению, у вас закончились жизни.")
                print(f"Загаданное слово было: {word.upper()}")

                while True:
                    cont = input("\nХотите продолжить игру? (да/нет): ").strip().lower()
                    if cont in ['да', 'нет']:
                        log_game_event(f"Игрок выбрал: '{cont}' после проигрыша")
                        break
                    print("Пожалуйста, введите 'да' или 'нет'")
                
                if cont == "да":
                    log_game_event("Перезапуск игры")
                    game_over = False
                    break
                else:
                    game_over = True
                    break
            else:
                log_game_event(f"Автоматический переход к следующему слову #{index+1}")
                continue
        
        if game_over:
            total_time = int(time.time() - start_time)
            minutes, seconds = divmod(total_time, 60)
            
            log_game_event(f"Игра завершена. Угадано слов: {guessed_words}, время: {minutes} мин {seconds} сек")

            print("\n=== ИГРА ЗАВЕРШЕНА ===")
            print("Спасибо за игру!")
            print("📊 Ваша статистика:")
            print(f"Угадано слов: {guessed_words}")
            print(f"Время игры: {minutes} мин {seconds} сек")
            print(f"Ваш лучший рекорд: {best_record} слов")

            if guessed_words > best_record:
                log_game_event(f"НОВЫЙ РЕКОРД! Старый: {best_record}, новый: {guessed_words}")
                print("\n🎊 НОВЫЙ РЕКОРД! 🎊")
                print("Вы установили новый личный рекорд!")
                print(f"Предыдущий рекорд: {best_record} слов")
                print(f"Новый рекорд: {guessed_words} слов")
                save_record(guessed_words)

            log_game_event("=== КОНЕЦ ИГРЫ ===")
            print("\nДо новых встреч в игре 'Поле чудес'!")
            input("\nНажмите Enter, чтобы выйти...")
            sys.exit()