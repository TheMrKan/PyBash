
class CommandExecutionError(Exception):
    """
    Предвиденная ошибка во время выполнения команды.
    Для них не выводится Traceback.
    """
    pass
