import os

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandCd(BaseCommand):
    NAME = 'cd'

    def __call__(self, path: str):
        try:
            os.chdir(path)
        except Exception as e:
            raise CommandExecutionError(str(e))
