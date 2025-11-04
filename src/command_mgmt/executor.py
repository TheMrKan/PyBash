from typing import Callable
from functools import wraps

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.base_command import BaseCommand


class CommandExecutor:

    def execute_command(self, command: BaseCommand, *args, **kwargs):
        print("Start executing")
        command(*args, **kwargs)
        print("Execution finished")

    def create_call_wrapper(self, factory: CommandFactory) -> Callable:
        tmp_instance = factory()

        @wraps(tmp_instance.__call__)  # type: ignore
        def wrapper(*args, **kwargs):
            self.execute_command(factory(), *args, **kwargs)

        return wrapper
