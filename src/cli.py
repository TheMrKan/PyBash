import typer
import logging
import os
import sys

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.source import DefaultCommandSource
from src.command_mgmt.executor import CommandExecutor


class CLI:
    """
    Основной класс. Отвечает за выполнение команды из sys.argv
    """
    __app: typer.Typer
    __logger: logging.Logger

    def __init__(self):
        self.__app = self.__build_typer_app()
        self.__logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        """
        Выполняет команду из sys.argv
        :raises SystemExit: ВСЕГДА вызывает SystemExit с exit code
        """
        self.__logger.info(f"{os.getcwd()} >>> {" ".join(sys.argv[1:])}")
        self.__app()
        raise SystemExit(0)

    def __build_typer_app(self) -> typer.Typer:
        # add_completion=False убирает мусор в --help
        _app = typer.Typer(add_completion=False)

        self.__register_commands(_app)

        return _app

    @staticmethod
    def __register_commands(_app: typer.Typer):
        """
        Регистрирует команды в Typer приложении все команды из источников.
        """

        # костыль. Без него Typer отказывается находить другие команды.
        # " " нужно, чтобы в --help не отображалось <function lambda ...
        _app.command(" ")(lambda: None)

        source = DefaultCommandSource()
        source.load_commands()

        executor = CommandExecutor()

        for cmd_class in source.commands:
            factory = CommandFactory(cmd_class)
            # Typer подразумевает, что все команды - это функции
            # app.command - это декоратор, принимающий название команды и регистрирующий функцию как команду
            # сама функция остается неизменной
            # в него передаем якобы функцию команды. На самом деле это вызов executor.execute_command
            # Typer внутри валидирует аргументы в соответствие с сигнатурой функции. Функция вызывается только если аргументы валидны
            # см. документацию к create_call_wrapper
            _app.command(cmd_class.NAME)(executor.create_call_wrapper(factory))
