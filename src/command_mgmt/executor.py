from typing import Callable
from functools import wraps
from rich import print
import logging

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandExecutor:

    __logger: logging.Logger

    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

    def execute_command(self, command: BaseCommand, *args, **kwargs):
        try:
            command(*args, **kwargs)
            self.__logger.info(f"OK")
        except CommandExecutionError as e:
            self.__logger.error(str(e))
            print(f"[red]ERROR >>> [/red]{str(e)}")
            raise SystemExit(1)
        except Exception as e:
            self.__logger.exception(f"An error occured during execution of command '{command.NAME}' with args {args} and kwargs {kwargs}", exc_info=e)
            print(f"[red]An error occured during execution of command '{command.NAME}' with args {args} and kwargs {kwargs}[/red]")
            raise SystemExit(1)

    def create_call_wrapper(self, factory: CommandFactory) -> Callable:
        tmp_instance = factory()

        @wraps(tmp_instance.__call__)  # type: ignore
        def wrapper(*args, **kwargs):
            self.execute_command(factory(), *args, **kwargs)

        return wrapper
