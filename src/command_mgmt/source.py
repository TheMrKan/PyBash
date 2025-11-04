import inspect
import pkgutil
import importlib
import logging

from src.command_mgmt.base_command import BaseCommand


class DefaultCommandSource:

    commands: list[type[BaseCommand]]

    __logger: logging.Logger

    def __init__(self):
        self.commands = []
        self.__logger = logging.getLogger(self.__class__.__name__)

    def load_commands(self):
        import src.commands
        self.commands.clear()

        for module_info in pkgutil.iter_modules(src.commands.__path__):
            module = importlib.import_module(src.commands.__name__ + "." + module_info.name)
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                    self.commands.append(obj)

        self.__logger.debug("Loaded %s commands from default source: %s", len(self.commands),
                            {c.NAME: c.__module__ + "." + c.__name__ for c in self.commands})
