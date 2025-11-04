from typing import TypeVar

from src.command_mgmt.base_command import BaseCommand

T = TypeVar("T", bound=BaseCommand)


class CommandFactory[T]:

    cmd_type: type[T]

    def __init__(self, cmd_type: type[T]):
        self.cmd_type = cmd_type

    def __call__(self) -> T:
        return self.cmd_type()
