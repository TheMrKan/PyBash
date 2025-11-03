from src.command_mgmt.base_command import BaseCommand


class CommandCd(BaseCommand):
    NAME = 'cd'

    def __call__(self, path: str):
        print(f"Cd {path}")
