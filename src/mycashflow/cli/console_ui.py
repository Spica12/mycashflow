from mycashflow.logging.logger import logger


class ConsoleUI:

    def __init__(self):
        pass

    def clear_screen(self):
        logger.debug("Clean screen")
        print("\033[2J\033[H", end="")

    def show(self, result: str = ""):
        logger.debug("result = %s", result)
        self.clear_screen()
        print("\n=")
        print(result)
        print("=\n")

    def greeting(self):
        logger.debug("Greeting!")
        self.show("Welcome to MyCashFlow")

    def exit(self):
        logger.debug("Good Bye")
        self.show("Good Bye!!!")
        exit()

    def run(self):

        self.greeting()

        while True:
            logger.debug('--- while ---')

            choice = input(">>>> ")
            logger.debug("choice = %s", choice)

            if choice.lower() == "exit":
                logger.debug("if exit")
                self.exit()

            self.show(choice)
