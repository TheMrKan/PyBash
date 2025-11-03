from typing import Callable, TypeVar
from functools import wraps

from src.command_mgmt.base_command import BaseCommand

T = TypeVar("T", bound=BaseCommand)


class CommandFactory[T]:

    cmd_type: type[T]

    def __init__(self, cmd_type: type[T]):
        self.cmd_type = cmd_type

    def __call__(self) -> T:
        return self.cmd_type()

    def create_call_wrapper(self) -> Callable:
        tmp_instance = self()

        @wraps(tmp_instance.__call__)    # type: ignore
        def wrapper(*args, **kwargs):
            return self()(*args, **kwargs)

        return wrapper
