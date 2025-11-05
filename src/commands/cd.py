import os
from pathlib import Path

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandCd(BaseCommand):
    """
    Переходит в указанную директорию.
    """

    NAME = 'cd'

    def __call__(self, path: Path):
        try:
            os.chdir(path)
        except Exception as e:
            raise CommandExecutionError(str(e))
