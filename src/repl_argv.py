import shlex
import contextlib
import sys
from typing import Callable


class REPLArgvRunner:

    __func: Callable

    def __init__(self, func: Callable):
        self.__func = func

    def run(self):
        while True:
            try:
                line = input("> ")
                parsed_args = shlex.split(line)

                with self.__with_argv(parsed_args):
                    try:
                        self.__func()
                    except SystemExit:
                        pass

            except KeyboardInterrupt:
                break

    @staticmethod
    @contextlib.contextmanager
    def __with_argv(args: list[str]):
        stack = []
        try:
            while len(sys.argv) > 1:
                stack.append(sys.argv.pop())
            sys.argv.extend(args)

            yield
        finally:
            while len(args) > 1:
                sys.argv.pop()
            sys.argv.extend(stack[::-1])
