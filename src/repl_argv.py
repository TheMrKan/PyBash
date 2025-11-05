import shlex
import contextlib
import sys
import os
import time
from typing import Callable, Any
import logging

from rich import print, get_console


class REPLArgvRunner:

    __func: Callable
    __logger: logging.Logger

    def __init__(self, func: Callable[[], Any]):
        """
        :param func: Callable, который будет вызываться с подмененными sys.argv на каждой итерации.
        """
        self.__func = func
        self.__logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def __get_prompt() -> str:
        """
        Возвращает строку, которая будет слева от ввода пользователя. Вроде аргумента input()
        """
        return f"[blue]{os.getcwd()} [/blue]>>> "

    def run(self):
        """
        Запускает бесконечный цикл ввода-выполнения-вывода. Выход через SIGINT
        """
        while True:
            parsed_args = ["?"]    # для вывода в последнем except
            try:
                # просто input() не подходит, т. к. это print из rich, поддерживающий форматированный вывод
                print(self.__get_prompt(), end="")
                line = input()
                if not line.strip():
                    continue

                parsed_args = shlex.split(line)

                # запускаем функцию с подмененными sys.argv
                with self.__with_argv(parsed_args):
                    try:
                        self.__func()
                    except SystemExit:    # CLI может возвращать через него exit code
                        pass

                # rich.print выводит с небольшой задержкой
                # если убрать sleep, то будет выводиться сначала промпт из следующей итерации, а потом вывод этой итерации
                time.sleep(0.05)

            except KeyboardInterrupt:
                break
            except Exception as e:
                get_console().print_exception()
                self.__logger.exception(f"An unhandled exception occured during invoking with argv: {parsed_args}", exc_info=e)

    @staticmethod
    @contextlib.contextmanager
    def __with_argv(args: list[str]):
        """
        Временно подменяет sys.argv.
        Не присваивает другой объект, а обновляет уже имеющийся список во избежание аномалий.
        При выходе возвращает sys.argv в состояние на момент входа.
        Не изменяет sys.argv[0] (путь до вызываемого файла).
        """
        # все единицы ниже связаны с игнорированием sys.argv[0]
        stack = []
        try:
            while len(sys.argv) > 1:
                stack.append(sys.argv.pop())
            sys.argv.extend(args)

            yield
        finally:
            while len(sys.argv) > 1:
                sys.argv.pop()
            sys.argv.extend(stack[::-1])
