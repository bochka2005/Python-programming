import sys
import cli_parser
import interactive_menu

def main():
    # Проверяем аргументы командной строки
    # Если их больше 1 (первый - это имя скрипта), пробуем CLI
    if len(sys.argv) > 1:
        ran_cli = cli_parser.run_cli_mode()
        # Если CLI вернул False (например, был флаг -i или нет команд), запускаем меню
        if not ran_cli:
            interactive_menu.run_menu()
    else:
        # Если аргументов нет вообще
        interactive_menu.run_menu()

if __name__ == "__main__":
    main()