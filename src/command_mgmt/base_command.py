from abc import ABC, abstractmethod


class BaseCommand(ABC):
    NAME: str = ""

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
