import sys
import logging


def __setup_logging():
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        level = logging.DEBUG
    else:
        level = logging.INFO
    sys.argv.remove("--debug")

    file_handler = logging.FileHandler(filename="../shell.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("[%(asctime)s %(levelname)s][%(name)s] %(message)s")
    file_handler.setFormatter(file_formatter)

    logging.root.setLevel(level)
    logging.root.addHandler(file_handler)


def main():
    __setup_logging()

    logger = logging.getLogger("main")
    logger.debug("Ran with args %s", sys.argv)

    from src.repl_argv import REPLArgvRunner
    from src.cli import CLI

    cli = CLI()

    if len(sys.argv) > 1:
        cli.run()
        return

    logger.debug("No argv found. Running REPL...")
    repl = REPLArgvRunner(cli.run)
    repl.run()


if __name__ == '__main__':
    main()
