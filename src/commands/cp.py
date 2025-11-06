from pathlib import Path
from rich import print
from typing import Annotated
import typer

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.fs_service import FileSystemService, ConfirmationRequiredError, FlagRequiredError
from src.utils.console import ask_confirmation


class CommandCp(BaseCommand):
    """
    Копирует файлы и директории
    """

    NAME = 'cp'

    def __call__(self, sources: list[Path], destination: Path, recursive: Annotated[bool, typer.Option("-r")] = False):
        errors = []
        try:
            gen = FileSystemService.copy_many(sources, destination, recursive=recursive)

            source, exception = next(gen)
            while True:
                to_send = None
                if isinstance(exception, ConfirmationRequiredError):
                    to_send = ask_confirmation(f"Do you want to override existing file with '{source}'?")
                elif isinstance(exception, FlagRequiredError):
                    print(f"[yellow]WARNING[/yellow] >>> Omitting directory '{source}' because '-r' is not specified.")
                elif isinstance(exception, OSError):
                    errors.append((source, exception))

                source, exception = gen.send(to_send)
                continue

        except StopIteration:
            pass
        except OSError as e:
            raise CommandExecutionError(str(e))

        for source, exception in errors:
            print(f"[red]ERROR[/red] >>> Failed to copy '{source}': {str(exception)}")

        # чтобы было сообщение в логе и для правильного exit code
        if any(errors):
            raise CommandExecutionError("One or more error occurred during command execution.")
