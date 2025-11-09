from typing import TypeVar
import logging

from src.command_mgmt.base_command import BaseCommand

T = TypeVar("T", bound=BaseCommand)


class CommandFactory[T]:

    cmd_type: type[T]

    def __init__(self, cmd_type: type[T]):
        self.cmd_type = cmd_type

    def __call__(self) -> T:
        logger = logging.getLogger(self.cmd_type.__name__)
        return self.cmd_type(logger)    # type: ignore
