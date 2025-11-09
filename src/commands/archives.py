from pathlib import Path

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.archive_service import ArchiveService


class CommandZip(BaseCommand):
    NAME = 'zip'

    def __call__(self, source: Path, destination: Path):
        try:
            ArchiveService().create_archive(source, destination, "zip")
        except Exception as e:
            raise CommandExecutionError(e)


class CommandTar(BaseCommand):
    NAME = 'tar'

    def __call__(self, source: Path, destination: Path):
        try:
            ArchiveService().create_archive(source, destination, "gztar")
        except Exception as e:
            raise CommandExecutionError(e)


class CommandUnzip(BaseCommand):
    NAME = 'unzip'

    def __call__(self, path: Path):
        try:
            ArchiveService().unarchive(path, "zip")
        except Exception as e:
            raise CommandExecutionError(e)


class CommandUntar(BaseCommand):
    NAME = 'untar'

    def __call__(self, path: Path):
        try:
            ArchiveService().unarchive(path, "gztar")
        except Exception as e:
            raise CommandExecutionError(e)
