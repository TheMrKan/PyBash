from typing import Callable
from functools import wraps
from rich import print
import logging

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandExecutor:
    """
    Отвечает за выполнение команд с переданными аргументами.
    Не занимается вылидацией аргументов и поиском команды.
    Подразумевается, что аргументы провалидированы ранее.
    """

    __logger: logging.Logger

    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

    def execute_command(self, command: BaseCommand, *args, **kwargs):
        """
        Вызывает command.__call__(*args, **kwargs) и обрабатывает исключения.
        Не валидирует аргументы.
        :raises SystemExit: При возникновении ошибки вызывает SystemExit с нужным exit code.
        """
        try:
            command(*args, **kwargs)
            self.__logger.info("OK")
        except CommandExecutionError as e:
            self.__logger.error(str(e))
            print(f"[red]ERROR >>> [/red]{str(e)}")
            raise SystemExit(1)
        except Exception as e:
            self.__logger.exception(f"An error occured during execution of command '{command.NAME}' with args {args} and kwargs {kwargs}", exc_info=e)
            print(f"[red]An error occured during execution of command '{command.NAME}' with args {args} and kwargs {kwargs}[/red]")
            raise SystemExit(1)

    def create_call_wrapper(self, factory: CommandFactory) -> Callable:
        """
        :return:
            Возвращает Callable с сигнатурой '__call__' команды, для которой передана фабрика.
            В сигнатуре отсутствует 'self'.
            Callable при вызове создает новый экземпляр команды через фабрику и вызывает 'CommandExecutor.execute_command' с экземпляром команды и всеми аргументами.
            Подходит для регистрации команд в фреймворках, где нужна чистая сигнатура функции.
        """
        # для получения сигнатуры __call__ без параметра self
        tmp_instance = factory()

        @wraps(tmp_instance.__call__)  # type: ignore
        def wrapper(*args, **kwargs):
            self.execute_command(factory(), *args, **kwargs)

        return wrapper
