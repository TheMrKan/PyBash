from pathlib import Path
import shutil
import logging


class ArchiveService:

    _logger: logging.Logger

    def __init__(self, logger: logging.Logger | None = None):
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    def create_archive(self, source: Path, destination: Path, arc_type: str):
        if not source.is_dir():
            raise Exception("Source is not an existing directory")

        path = str(destination.parent / destination.stem)
        shutil.make_archive(path, arc_type, source, logger=self._logger)

    @staticmethod
    def unarchive(path: Path, fmt: str):
        shutil.unpack_archive(str(path), format=fmt)
