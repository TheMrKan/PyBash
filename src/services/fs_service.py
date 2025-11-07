from pathlib import Path
import shutil
import stat
import os
from typing import Generator, Any


class ConfirmationRequiredError(Exception):
    """
    Операция требует подтверждения от пользователя.
    После подтверждения функция должна быть вызвана повторно с соответствующим флагом.
    """
    pass


class FlagRequiredError(Exception):
    """
    Операция не требует подтверждения, но не может быть выполнена без указания специального флага.
    """
    pass


class FileSystemService:
    """
    Сервис операций с файловой системой.
    """

    @staticmethod
    def is_hidden(path: Path) -> bool:
        """
        Проверяет, является ли объект скрытым.
        """
        if path.name.startswith("."):
            return True

        # для Windows
        if path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
            return True

        return False

    @staticmethod
    def copy(source: Path, destination: Path,
             recursive: bool = False, override: bool = False):
        """
        Копирует объект.
        Перезапись только с 'override' = True. Копирование директорий только с 'recursive' = True.
        Если целевой объект - существующая директория, то копирует объект внутрь с тем же именем.
        :param recursive: Разрешает копирование директорий со всем содержимым.
        :param override: Разрешает перезапись объектов.
        :raises ConfirmationRequiredError: Попытка перезаписать существующий объект без 'override' = True.
        :raises FlagRequiredError: Попытка рекурсивно скопировать директорию без 'recursive' = True.
        """

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
        """
        Поочередно копирует все объекты 'sources' в 'destination'. При возникновении предвиденного исключения переходит к следующему элементу.
        :param recursive: Разрешает копирование директорий со всем содержимым.
        :return:
            Кортеж (path, exception) для каждого объекта, при копировании которого возникло предвиденное исключение.
            ConfirmationRequiredError - запрос подтверждения на перезапись объекта. Ожидает bool в качестве ответа. Если bool(value) == True, то повторяет операцию с подтверждением на перезапись.
            FlagRequiredError - копирование объекта пропущено из-за отсутствия флага на рекурсивное копирование. Не ожидает ответа.
            OSError - любое исключение ОС, возникшее при копировании объекта.
        """
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
        """
        Перемещает или переименовывает объект. Перезапись существующего объекта только при 'override' = True.
        Если 'destination' - существующая директория, то перемещает внутрь с исходным названием.
        :param override: Разрешает перезапись существующего файла.
        :raises FlagRequiredError: Попытка перезаписи объекта без 'override' = True.
        """

        if destination.is_dir():
            overriding = (destination / source.name).exists()
        else:
            overriding = destination.exists()

        if overriding and not override:
            raise FlagRequiredError("Destination already exists, 'override' must be True")

        shutil.move(source, destination)

    @classmethod
    def remove(cls, item: Path, recursive: bool = False):
        """
        Удаляет объект. Удаление директорий только с 'recursive' = True.
        :param recursive: Разрешает удаление непустых директорий.
        :raises FlagRequiredError: Попытка удаления непустой директории без 'recursive' = True.
        """
        cls.__assert_is_not_anchor(item)
        cls.__assert_is_not_parent(item, Path.cwd())

        if item.is_dir() and any(item.iterdir()) and not recursive:
            raise FlagRequiredError("Can't remove a non-empty directory with 'recursive' = False.")

        if item.is_dir():
            shutil.rmtree(item)
        else:
            os.remove(item)

    @staticmethod
    def __assert_is_not_parent(potential_parent: Path, path: Path):
        """
        Вызывает исключение, если 'path' является дочерним путём для 'potential_parent'.
        Иными словами, исключение если 'path' находится внутри 'potential_parent'.
        :raises OSError: 'potential_parent' является одним из родителей 'path'
        """
        while not path.parent.samefile(path):
            if path.samefile(potential_parent):
                raise OSError("Operation is not allowed with parent directory.")

            path = path.parent

    @staticmethod
    def __assert_is_not_anchor(path: Path):
        """
        Вызывает исключение, если 'path' является корневым каталогом.
        Например '/' или 'C:/'.
        :raises OSError: 'path' является корневым каталогом.
        """
        if path.samefile(path.anchor):
            raise OSError("Operation is not allowed with root path.")
