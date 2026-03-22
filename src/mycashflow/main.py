from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage
from mycashflow.models.transaction import Transaction
from mycashflow.cli.console_ui import ConsoleUI







if __name__ == "__main__":
    cli = ConsoleUI()
    cli.run()
