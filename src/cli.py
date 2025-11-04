import typer
import logging
import os
import sys

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.source import DefaultCommandSource
from src.command_mgmt.executor import CommandExecutor


class CLI:
    app: typer.Typer
    __logger: logging.Logger

    def __init__(self):
        self.app = self.__build_app()
        self.__logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        self.__logger.info(f"{os.getcwd()} >>> {" ".join(sys.argv[1:])}")
        self.app()

    def __build_app(self) -> typer.Typer:
        _app = typer.Typer(add_completion=False)

        self.__register_commands(_app)

        return _app

    @staticmethod
    def __register_commands(_app: typer.Typer):
        _app.command(" ")(lambda: None)

        source = DefaultCommandSource()
        source.load_commands()

        executor = CommandExecutor()

        for cmd_class in source.commands:
            factory = CommandFactory(cmd_class)
            _app.command(cmd_class.NAME)(executor.create_call_wrapper(factory))
