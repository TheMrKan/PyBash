import typer

from src.command_mgmt.command_factory import CommandFactory
from src.command_mgmt.source import DefaultSource
from src.command_mgmt.base_command import BaseCommand


app: typer.Typer


def build_app() -> typer.Typer:
    _app = typer.Typer(add_completion=False)

    __register_commands(_app)

    return _app


def __register_commands(_app: typer.Typer):
    _app.command(" ")(lambda: None)

    source = DefaultSource()
    source.load_commands()

    for cmd_class in source.commands:
        __register_command(_app, cmd_class)


def __register_command(_app: typer.Typer, cmd_class: type[BaseCommand]):
    factory = CommandFactory(cmd_class)
    _app.command(cmd_class.NAME)(factory.create_call_wrapper())
