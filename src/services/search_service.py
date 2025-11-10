import logging
from pathlib import Path
import re
from dataclasses import dataclass


@dataclass
class SearchResultLine:
    line_num: int
    line_content: str

    def __eq__(self, other):
        return (self.line_num == other.line_num
                and self.line_content == other.line_content)


class FileSearchResult:
    file_path: Path
    fragments: list[SearchResultLine]

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.fragments = []


class SearchService:

    _logger: logging.Logger

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def find_in_file(self, filepath: Path, pattern: str, case_insensitive: bool = False) -> FileSearchResult:
        if not filepath.is_file():
            raise IsADirectoryError(f"File {filepath} is not a file")

        result = FileSearchResult(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            for line_index, line in enumerate(f):
                if case_insensitive:
                    flag = re.IGNORECASE
                else:
                    flag = 0    # type: ignore

                found = tuple(re.finditer(pattern, line, flags=flag))
                if not any(found):
                    continue

                line_obj = SearchResultLine(line_index+1, line)
                result.fragments.append(line_obj)
        return result

    def find_in_files_recursively(self, source: Path, pattern: str, case_insensitive: bool = False) -> list[FileSearchResult]:
        if not source.is_dir():
            raise NotADirectoryError(str(source))

        result = []
        for file in (p for p in source.rglob("*") if p.is_file()):
            try:
                res = self.find_in_file(file, pattern, case_insensitive=case_insensitive)
                if any(res.fragments):
                    result.append(res)
            except Exception as e:
                self._logger.exception("Failed to find in file", exc_info=e)

        return result
