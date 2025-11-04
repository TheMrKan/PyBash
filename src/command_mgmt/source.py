import inspect
import pkgutil
import importlib

from src.command_mgmt.base_command import BaseCommand


class DefaultSource:

    commands: list[type[BaseCommand]]

    def __init__(self):
        self.commands = []

    def load_commands(self):
        import src.commands
        self.commands.clear()

        for module_info in pkgutil.iter_modules(src.commands.__path__):
            module = importlib.import_module(src.commands.__name__ + "." + module_info.name)
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                    self.commands.append(obj)
