from pathlib import Path
import shutil
import stat
from typing import Generator, Any


class ConfirmationRequiredError(Exception):
    pass


class FlagRequiredError(Exception):
    pass


class FileSystemService:

    @staticmethod
    def is_hidden(path: Path) -> bool:
        if path.name.startswith("."):
            return True

        # для Windows
        if path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
            return True

        return False

    @staticmethod
    def copy(source: Path, destination: Path,
             recursive: bool = False, override: bool = False):

        overriding = destination.is_file() or (destination.is_dir() and (destination / source.name).exists())
        if overriding and not override:
            raise ConfirmationRequiredError("Destination file already exists, 'override' must be True")

        if source.is_dir() and not recursive:
            raise FlagRequiredError(f"'{source.name}' is a directory, 'recursive' must be True")

        if source.is_dir():
            if destination.is_dir():
                shutil.copytree(source, destination / source.name, dirs_exist_ok=True)
            else:
                shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy(source, destination)

    @classmethod
    def copy_many(cls, sources: list[Path], destination: Path, recursive: bool = False) \
            -> Generator[tuple[Path, Exception], Any, None]:
        if not destination.is_dir() and len(sources) != 1:
            raise OSError("Can't copy many object to one file")

        for source in sources:
            try:
                cls.copy(source, destination, recursive=recursive)
            except ConfirmationRequiredError as e:
                confirmed = yield source, e
                if confirmed:
                    cls.copy(source, destination, recursive=recursive, override=True)
            except FlagRequiredError as e:
                yield source, e
            except OSError as e:
                yield source, e

    @staticmethod
    def move(source: Path, destination: Path, override: bool = False):

        if destination.is_dir():
            overriding = (destination / source.name).exists()
        else:
            overriding = destination.exists()

        if overriding and not override:
            raise FlagRequiredError("Destination already exists, 'override' must be True")

        shutil.move(source, destination)
