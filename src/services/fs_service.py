from pathlib import Path
import stat


class FileSystemService:

    @staticmethod
    def is_hidden(path: Path) -> bool:
        if path.name.startswith("."):
            return True

        # для Windows
        if path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
            return True

        return False