from pathlib import Path
import typer
from typing import Annotated
from rich import print

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.fs_service import FileSystemService, FlagRequiredError, ConfirmationRequiredError
from src.utils.console import ask_confirmation


class CommandRm(BaseCommand):
    """
    Удаляет файл или директорию
    """
    NAME = "rm"

    def __call__(self, items: list[Path], recursive: Annotated[bool, typer.Option("-r")] = False):
        error_occured = False

        for item in items:
            try:
                FileSystemService.remove(item, recursive=recursive)
            except FlagRequiredError:
                print(f"[yellow]WARNING[/yellow] >>> Omitting '{item}' because '-r' is not specified.")
                error_occured = True
            except ConfirmationRequiredError:
                if ask_confirmation(f"Do you want to remove directory '{item}'?"):
                    FileSystemService.remove(item, recursive=recursive, confirmed=True)
            except OSError as e:
                print(f"[red]ERROR[/red] >>> Failed to remove '{item}': {str(e)}")
                error_occured = True

        if error_occured:
            raise CommandExecutionError("One or more errors occured during command execution.")
