import sys
import logging


def __setup_logging():
    """
    Глобальная настройка логгирования
    """

    # sys.argv[0] - всегда путь до файла
    # проверяем 'sys.argv[1] ==' чтобы не могло быть конфликтов с параметрами команд
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        level = logging.DEBUG
        sys.argv.remove("--debug")
    else:
        level = logging.INFO

    # ../ т. к. при вызове модуля текущая директория - src, а лог должен быть уровнем выше
    file_handler = logging.FileHandler(filename="../shell.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("[%(asctime)s %(levelname)s][%(name)s] %(message)s")
    file_handler.setFormatter(file_formatter)

    logging.root.setLevel(level)
    logging.root.addHandler(file_handler)


def main():
    """
    Точка входа. Подготавливает окружение; в зависимости от аргументов запускает конкретную команду или REPL.
    """
    __setup_logging()

    logger = logging.getLogger("main")
    logger.debug("Ran with args %s", sys.argv)

    # на всякий случай настройки логгинга до импортов
    # на случай вызовов getLogger в глобальном скоупе
    from src.repl_argv import REPLArgvRunner
    from src.cli import CLI

    cli = CLI()

    # если переданы аргументы, то пытаемся их интерпретировать как команду
    # >1, т. к. sys.argv[0] - путь до файла
    if len(sys.argv) > 1:
        cli.run()
        return

    # если аргументов нет, то запускаем интерактивную оболочку
    logger.debug("No argv found. Running REPL...")
    repl = REPLArgvRunner(cli.run)
    repl.run()


if __name__ == '__main__':
    main()
