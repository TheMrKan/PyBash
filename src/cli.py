import typer

from src.command_mgmt.command_factory import CommandFactory
from src.commands.cd import CommandCd


app: typer.Typer


def build_app() -> typer.Typer:
    _app = typer.Typer(add_completion=False)

    __register_commands(_app)

    return _app


def __register_commands(_app: typer.Typer):
    cls = CommandCd

    _app.command(" ")(lambda: None)
    factory = CommandFactory(CommandCd)
    _app.command(cls.NAME)(factory.create_call_wrapper())
