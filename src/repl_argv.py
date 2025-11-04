import shlex
import contextlib
import sys
import os
import time
from typing import Callable
from rich import print


class REPLArgvRunner:

    __func: Callable

    def __init__(self, func: Callable):
        self.__func = func

    @staticmethod
    def __get_prompt():
        return f"[blue]{os.getcwd()} [/blue]> "

    def run(self):
        while True:
            try:
                print(self.__get_prompt(), end="")
                line = input()
                if not line.strip():
                    continue

                parsed_args = shlex.split(line)

                with self.__with_argv(parsed_args):
                    try:
                        self.__func()
                    except SystemExit:
                        pass

                time.sleep(0.05)

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
            while len(sys.argv) > 1:
                sys.argv.pop()
            sys.argv.extend(stack[::-1])
