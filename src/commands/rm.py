from pathlib import Path
import typer
from typing import Annotated

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.fs_service import FileSystemService, FlagRequiredError


class CommandRm(BaseCommand):
    """
    Удаляет файл или директорию
    """
    NAME = "rm"

    def __call__(self, item: Path, recursive: Annotated[bool, typer.Option("-r")] = False):
        try:
            FileSystemService.remove(item, recursive=recursive)
        except FlagRequiredError:
            raise CommandExecutionError("Flag '-r' is required to remove directories")
        except OSError as e:
            raise CommandExecutionError(str(e))
