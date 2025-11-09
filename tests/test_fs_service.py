from pathlib import Path
from typing import Generator
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher
import os

from src.services.fs_service import FileSystemService, FlagRequiredError, ConfirmationRequiredError


@pytest.fixture
def filesystem() -> Generator[Patcher, None, None]:
    with Patcher() as p:
        yield p


@pytest.fixture
def fake_files(filesystem: Patcher):
    filesystem.fs.create_file('/tmp/file1.txt').set_contents("Content 1")
    filesystem.fs.create_file('/tmp/file2.txt').set_contents("Content 2")
    filesystem.fs.create_file('/tmp/file3.txt').set_contents("Content 3")

    filesystem.fs.create_dir("/tmp/dir1")
    filesystem.fs.create_file('/tmp/dir1/file1.txt').set_contents("Content 1 1")
    filesystem.fs.create_file('/tmp/dir1/file2.txt').set_contents("Content 1 2")

    filesystem.fs.create_dir("/tmp/dir2")
    filesystem.fs.create_file('/tmp/dir2/file1.txt').set_contents("Content 2 1")
    filesystem.fs.create_file('/tmp/dir2/file2.txt').set_contents("Content 2 2")

    filesystem.fs.create_dir("/usr")
    filesystem.fs.create_dir("/usr/bin")

    os.chdir("/tmp")


class TestCopy:
    def test_basic(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/file4.txt')
        FileSystemService.copy(src, dst)
        assert dst.exists()
        assert dst.read_text() == "Content 1"

    def test_copy_dir(self, fake_files):
        src = Path('/tmp/dir1')
        dst = Path('/tmp/dir3')
        with pytest.raises(FlagRequiredError):
            FileSystemService.copy(src, dst)

    def test_copy_dir_confirmed(self, fake_files):
        src = Path('/tmp/dir1')
        dst = Path('/tmp/dir3')
        FileSystemService.copy(src, dst, recursive=True)
        assert dst.exists()
        assert os.listdir(src) == os.listdir(dst)

    def test_override_basic(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/file2.txt')
        with pytest.raises(ConfirmationRequiredError):
            FileSystemService.copy(src, dst)

    def test_override_nested(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/dir1/file1.txt')
        with pytest.raises(ConfirmationRequiredError):
            FileSystemService.copy(src, dst)

    def test_override_confirmed(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/file2.txt')
        FileSystemService.copy(src, dst, override=True)
        assert dst.exists()
        assert dst.read_text() == "Content 1"

    def test_copy_to_dir(self, fake_files):
        src = Path('/tmp/file3.txt')
        dst = Path('/tmp/dir1')

        FileSystemService.move(src, dst)
        assert (dst / "file3.txt").exists()
        assert (dst / "file3.txt").read_text() == "Content 3"


class TestMove:

    def test_basic(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/file4.txt')

        FileSystemService.move(src, dst)
        assert not src.exists()
        assert dst.exists()
        assert dst.read_text() == "Content 1"

    def test_override_basic(self, fake_files):
        src = Path("/tmp/file1.txt")
        dst = Path("/tmp/file2.txt")

        with pytest.raises(ConfirmationRequiredError):
            FileSystemService.copy(src, dst)

    def test_override_nested(self, fake_files):
        src = Path("/tmp/file1.txt")
        dst = Path("/tmp/dir1/file1.txt")

        with pytest.raises(ConfirmationRequiredError):
            FileSystemService.copy(src, dst)

    def test_override_confirmed(self, fake_files):
        src = Path('/tmp/file1.txt')
        dst = Path('/tmp/file2.txt')

        FileSystemService.move(src, dst, override=True)
        assert not src.exists()
        assert dst.exists()
        assert dst.read_text() == "Content 1"

    def test_move_to_dir(self, fake_files):
        src = Path('/tmp/file3.txt')
        dst = Path('/tmp/dir1')

        FileSystemService.move(src, dst)
        assert not src.exists()
        assert (dst / "file3.txt").exists()
        assert (dst / "file3.txt").read_text() == "Content 3"


class TestAsserts:

    def test_parent_positive(self, fake_files):
        path1 = Path("/tmp")
        path2 = Path("/usr")
        FileSystemService._FileSystemService__assert_is_not_parent(path1, path2)    # type: ignore

    @pytest.mark.parametrize("path1, path2", [("/", "/tmp"), ("/usr", "/usr/bin"), ("/tmp/dir1/../", "/tmp/dir2")])
    def test_parent_raises(self, fake_files, path1: str, path2: str):
        with pytest.raises(OSError):
            FileSystemService._FileSystemService__assert_is_not_parent(Path(path1), Path(path2))    # type: ignore

    def test_anchor_positive(self, fake_files):
        FileSystemService._FileSystemService__assert_is_not_anchor(Path("/tmp"))    # type: ignore

    @pytest.mark.parametrize("path", ["/", "//", "C://", "F:/", "/tmp/.."])
    def test_anchor_raises(self, fake_files, path: str):
        with pytest.raises(OSError):
            FileSystemService._FileSystemService__assert_is_not_anchor(Path(path))    # type: ignore


class TestRemove:

    @pytest.fixture
    def asserts(self, mocker):
        mocker.patch("src.services.fs_service.FileSystemService._FileSystemService__assert_is_not_parent")
        mocker.patch("src.services.fs_service.FileSystemService._FileSystemService__assert_is_not_anchor")
        yield
        FileSystemService._FileSystemService__assert_is_not_parent.assert_called()    # type: ignore
        FileSystemService._FileSystemService__assert_is_not_anchor.assert_called()    # type: ignore

    def test_basic(self, fake_files, asserts):
        path = Path("/tmp/file1.txt")
        FileSystemService.remove(path)
        assert not path.exists()

    def test_recursive(self, fake_files, asserts):
        path = Path("/tmp/dir1")
        with pytest.raises(FlagRequiredError):
            FileSystemService.remove(path)
        assert path.exists()

    def test_recursive_confirmed(self, fake_files, asserts):
        path = Path("/tmp/dir1")
        with pytest.raises(ConfirmationRequiredError):
            FileSystemService.remove(path, recursive=True)
        assert path.exists()

    def test_directory_confirmed(self, fake_files, asserts):
        path = Path("/tmp/dir1")
        FileSystemService.remove(path, recursive=True, confirmed=True)
        assert not path.exists()
