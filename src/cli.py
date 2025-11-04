import typer

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.source import DefaultCommandSource
from src.command_mgmt.executor import CommandExecutor


app: typer.Typer


def build_app() -> typer.Typer:
    _app = typer.Typer(add_completion=False)

    __register_commands(_app)

    return _app


def __register_commands(_app: typer.Typer):
    _app.command(" ")(lambda: None)

    source = DefaultCommandSource()
    source.load_commands()

    executor = CommandExecutor()

    for cmd_class in source.commands:
        factory = CommandFactory(cmd_class)
        _app.command(cmd_class.NAME)(executor.create_call_wrapper(factory))
