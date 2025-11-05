import typer
from pathlib import Path
import datetime
import stat
from rich import print
from rich.text import Text
from rich.table import Table
from typing import Annotated, Iterable, Generator

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.fs_service import FileSystemService


class CommandLs(BaseCommand):
    NAME = "ls"

    def __call__(self,
                 path: Annotated[Path | None, typer.Argument(show_default=False)] = None,
                 verbose: Annotated[bool, typer.Option("-l", is_flag=True)] = False,
                 ) -> None:
        if not path:
            path = Path.cwd()

        source = self.__filter_objects(path.iterdir())

        try:
            if verbose:
                self.__list_verbose(str(path), source)
            else:
                self.__list_short(source)
        except OSError as e:
            raise CommandExecutionError(str(e))

    @staticmethod
    def __filter_objects(source: Iterable[Path]) -> Generator[Path, None, None]:
        for obj in source:
            if FileSystemService.is_hidden(obj):
                continue

            yield obj

    @staticmethod
    def __select_style_for_obj(path: Path) -> str:
        if path.is_dir():
            return "green"
        return ""

    def __list_short(self, source: Iterable[Path]) -> None:
        for obj in source:
            print(Text(obj.name, self.__select_style_for_obj(obj)))

    def __list_verbose(self, title: str, source: Iterable[Path]) -> None:
        table = Table(title=title)

        table.add_column("Perms", width=9)
        table.add_column("Size", justify="right")
        table.add_column("Modified", justify="right")
        table.add_column("Name", justify="left")

        for obj in source:
            table.add_row(self.__format_permissions(obj.stat().st_mode),
                          self.__format_size(obj.stat().st_size),
                          self.__format_modified_time(obj.stat().st_mtime),
                          obj.name,
                          style=self.__select_style_for_obj(obj)
                          )

        print(table)

    @staticmethod
    def __format_size(size_bytes: int) -> str:
        for lit in ("B", "KB", "MB", "GB", "TB"):
            if size_bytes < 1024:
                break
            size_bytes /= 1024

        return f"{size_bytes:.2f} {lit: >2}"

    @staticmethod
    def __format_permissions(st_mode: int) -> str:
        result = ["-"] * 9

        for idx, (flag, lit) in enumerate((
                (stat.S_IRUSR, "r"), (stat.S_IWUSR, "w"), (stat.S_IXUSR, "x"),
                (stat.S_IRGRP, "r"), (stat.S_IWGRP, "w"), (stat.S_IXGRP, "x"),
                (stat.S_IROTH, "r"), (stat.S_IWOTH, "w"), (stat.S_IXOTH, "x")
        )):
            if flag & st_mode:
                result[idx] = lit

        return "".join(result)

    @staticmethod
    def __format_modified_time(timestamp: float) -> str:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


