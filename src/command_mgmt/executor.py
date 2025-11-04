from typing import Callable
from functools import wraps
import traceback

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandExecutor:

    def execute_command(self, command: BaseCommand, *args, **kwargs):

        try:
            command(*args, **kwargs)
        except CommandExecutionError as e:
            print(f"ERROR >>> {e}")
            raise SystemExit(1)
        except Exception as e:
            print(f"An error occured during execution of command '{command.NAME}' with args {args} and kwargs {kwargs}")
            traceback.print_exception(e)
            raise SystemExit(1)

    def create_call_wrapper(self, factory: CommandFactory) -> Callable:
        tmp_instance = factory()

        @wraps(tmp_instance.__call__)  # type: ignore
        def wrapper(*args, **kwargs):
            self.execute_command(factory(), *args, **kwargs)

        return wrapper
