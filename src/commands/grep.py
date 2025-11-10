from pathlib import Path
from typer import Option
from typing import Annotated
from rich import print

from src.command_mgmt.base_command import BaseCommand
from src.command_mgmt.exceptions import CommandExecutionError
from src.services.search_service import SearchService, FileSearchResult


class CommandGrep(BaseCommand):
    NAME = "grep"

    def __call__(self, pattern: str, path: Path,
                 recursive: Annotated[bool, Option("-r")] = False,
                 case_insensitive: Annotated[bool, Option("-i")] = False):

        try:
            if recursive:
                result = SearchService().find_in_files_recursively(path, pattern, case_insensitive=case_insensitive)
            else:
                result = [SearchService().find_in_file(path, pattern, case_insensitive=case_insensitive)]
        except Exception as e:
            raise CommandExecutionError(e)

        if not any(result):
            print("No matches found")
            return

        for file in result:
            self.__print_file_result(file)

    @staticmethod
    def __print_file_result(file_result: FileSearchResult):
        print(f"[green]{file_result.file_path.absolute()}[/green]\n")

        for fragment in file_result.fragments:
            print(f"Line {fragment.line_num} >>> {fragment.line_content.strip()}")

        print("\n\n")
