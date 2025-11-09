from abc import ABC, abstractmethod
import logging


class BaseCommand(ABC):
    """
    Базовый класс для всех команд.
    """

    NAME: str = ""
    """
    Название команды, по которому она будет вызываться. Без пробелов и спец символов, желательно в нижнем регистре.
    """

    _logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Логика выполнения команды.
        Можно указывать конкретные аргументы. Валидация аргументов происходит по сигнатуре до вызова функции.
        """
        pass
