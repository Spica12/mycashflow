import subprocess
import sys

from pathlib import Path

from mycashflow.models.transaction import Transaction, entries
from mycashflow.storage.storage import JSONStorage
from mycashflow.logging.logger import logger


class Button:
    def __init__(self, text: str, callback):
        """
        :param text: текст кнопки у меню
        :param callback: функція, яка викликається при виборі
        """
        self.text = text
        self.callback = callback # функція або Menu


class Menu:

    def __init__(self, title: str, main_menu = None):
        self.title = title
        self.buttons = []
        self.main_menu = main_menu

        # кнопки назад/вихід не додаємо в self.buttons відразу
        self.back_button = Button(f"Назад до {main_menu.title}", self.main_menu) if main_menu else None
        self.exit_button = Button("Вийти", exit)

    def add_button(self, button: Button):
        self.buttons.append(button)


class ConsoleUI:

    def __init__(self):
        self.storage = JSONStorage("transactions.json")
        self.transactions = self.storage.load()

        self.main_menu = Menu("Головне меню")
        self.sub_menu = Menu("Підменю", main_menu=self.main_menu)

        self.main_menu.add_button(Button(f"Відкрити {self.sub_menu.title}", self.sub_menu))
        self.sub_menu.add_button(Button("Скажи Привіт", lambda: "Hello!"))

    def display_output(self, result: str = ""):
        if result:
            len_result: int = len(result)
            print(f"\n{"="*len_result}")
            print(result)
            print(f"{"="*len_result}")

    def display_menu(self, transaction: Transaction):
        len_buttons = len(transaction.entries)
        
        for i, button in enumerate(len_buttons, start=1):
            print(f"{i}. {button.text}")

        if menu.back_button:
            print(f"0. {menu.back_button.text}")

    def clear_screen(self):
        print("\033[2J\033[H", end="")

    def show(self, result, menu):
        self.clear_screen()
        self.display_output(result)
        self.display_menu(menu)

    def exit(self) -> None:
        exit()

    def load_transaction(self, id: int) -> Transaction:
        data = JSONStorage().load_transaction(id)

        transaction: Transaction = Transaction(
            id = data["id"]
            group = data["group"],
        )
        for entry in data["entries"]:
            transaction.add_entry(account=entry["account"], amount=entry["amount"]])

        return transaction


    def run(self):

        current_menu: Menu = self.main_menu
        current_result: str = current_menu.title

        while True:  # робимо петлю, щоб можна було повертатися
            logger.debug("current menu = %s", current_menu.title)
            logger.debug("current_result = %s", current_result)

            self.show(current_result, current_menu)

            choice = input(">>>> ")
            logger.debug("choice = %s", choice)
            try:
                if choice.lower() == "0":
                    current_menu = current_menu.main_menu
                    current_result = current_menu.title

                elif choice.lower() == "exit":
                    return self.exit()
                else:
                    idx = int(choice) - 1
                    if 0 <= idx < len(current_menu.buttons):
                        target = current_menu.buttons[idx].callback
                        if isinstance(target, Menu):
                            current_menu = target  # відкриваємо підменю
                            current_result = current_menu.title
                        else:
                            current_result: str = target()  # викликаємо функцію
                            logger.debug("current_result = %s", current_result)
                    else:
                        print("Невірний вибір")
            except ValueError:
                print("Введіть число")
