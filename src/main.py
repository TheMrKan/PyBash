import sys

from src.repl_argv import REPLArgvRunner
from src import cli


def main():
    cli.app = cli.build_app()

    if len(sys.argv) > 1:
        cli.app()
        return

    repl = REPLArgvRunner(cli.app)
    repl.run()


if __name__ == '__main__':
    main()
