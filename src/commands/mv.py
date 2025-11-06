from pathlib import Path

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.fs_service import FileSystemService, FlagRequiredError
from src.utils.console import ask_confirmation


class CommandMv(BaseCommand):
    """
    Перемещает/переименовывает объект.
    """
    NAME = "mv"

    def __call__(self, source: Path, destination: Path):
        try:
            try:
                FileSystemService.move(source, destination)
            except FlagRequiredError:
                confirmation = ask_confirmation(f"Do you want to override existing file or directory with '{source}'?")
                if confirmation:
                    FileSystemService.move(source, destination, override=True)
        except OSError as e:
            raise CommandExecutionError(str(e))
