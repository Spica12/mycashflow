from mycashflow.logging.logger import logger
from mycashflow.cli.console_ui import ConsoleUI


def main():
    cli = ConsoleUI()
    cli.run()

if __name__ == "__main__":
    main()
