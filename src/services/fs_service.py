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
             recursive: bool = False, override_confirmed: bool = False):

        overriding = destination.is_file() or (destination.is_dir() and (destination / source).is_file())
        if overriding and not override_confirmed:
            raise ConfirmationRequiredError("Destination file already exists, 'override_confirmed' must be True")

        if source.is_dir() and not recursive:
            raise FlagRequiredError(f"'{source.name}' is a directory, 'recursive' must be True")

        if source.is_dir():
            shutil.copytree(source, destination / source, dirs_exist_ok=True)
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
                    cls.copy(source, destination, recursive=recursive, override_confirmed=True)
            except FlagRequiredError as e:
                yield source, e
            except OSError as e:
                yield source, e
