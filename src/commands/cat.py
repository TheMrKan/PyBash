from pathlib import Path
from rich import print

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError


class CommandCat(BaseCommand):

    NAME = 'cat'

    def __call__(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            raise CommandExecutionError(str(e))
