import pytest
from pyfakefs.fake_filesystem_unittest import Patcher
from typing import Generator
import os
from pathlib import Path

from src.services.search_service import SearchService, SearchResultLine


@pytest.fixture
def filesystem() -> Generator[Patcher, None, None]:
    with Patcher() as p:
        yield p


@pytest.fixture
def fake_files(filesystem: Patcher):
    filesystem.fs.create_dir("/tmp")

    filesystem.fs.create_file("/tmp/test.txt").set_contents("Line 1\nLine 2\nTest data on line 3")
    filesystem.fs.create_file("/tmp/test2.txt").set_contents("Not line\n123\n456\nLine 4")

    os.chdir("/tmp")


class TestFindInFile:

    def test_find_basic(self, fake_files):
        source = Path("/tmp/test.txt")

        result = SearchService().find_in_file(source, "Line")
        assert result.file_path == source
        assert len(result.fragments) == 2

        assert result.fragments[0] == SearchResultLine(1, "Line 1\n")
        assert result.fragments[1] == SearchResultLine(2, "Line 2\n")

    def test_find_insensitive(self, fake_files):
        source = Path("/tmp/test.txt")

        result = SearchService().find_in_file(source, "Line", case_insensitive=True)
        assert result.file_path == source
        assert len(result.fragments) == 3

        assert result.fragments[0] == SearchResultLine(1, "Line 1\n")
        assert result.fragments[1] == SearchResultLine(2, "Line 2\n")
        assert result.fragments[2] == SearchResultLine(3, "Test data on line 3")

    def test_not_found(self, fake_files):
        source = Path("/tmp/test.txt")

        result = SearchService().find_in_file(source, "Not found", case_insensitive=True)
        assert result.file_path == source
        assert len(result.fragments) == 0


class TestFindRecursively:
    def test_find_basic(self, fake_files):
        source = Path("/tmp")

        result = SearchService().find_in_files_recursively(source, "Line")
        assert len(result) == 2

        assert result[0].fragments[0] == SearchResultLine(1, "Line 1\n")
        assert result[0].fragments[1] == SearchResultLine(2, "Line 2\n")

        assert result[1].fragments[0] == SearchResultLine(4, "Line 4")

    def test_on_file(self):
        source = Path("/tmp/test.txt")

        with pytest.raises(NotADirectoryError):
            SearchService().find_in_files_recursively(source, "Line")
