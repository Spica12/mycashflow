from dataclasses import dataclass, field

from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage
from mycashflow.models.transaction import Transaction
from mycashflow.services.transaction_service import TransactionManager


class ConsoleUI:

    def __init__(self):
        self.manager = TransactionManager()
        self.current_transaction = self.manager.get_by_id(1)
        if self.current_transaction is None:
            self.add_transaction()

        self.result = ""

    def clear_screen(self):
        logger.debug("Clean screen")
        print("\033[2J\033[H", end="")

    def display_current_transaction(self):
        logger.debug("transaction = %s", self.current_transaction)
        print("\n=")
        deep = self._get_max_deep_tree(self.current_transaction, deep=0) + 1
        deep = 2 + deep * 3 + 7
        print(self._build_tree(transaction=self.current_transaction, deep=deep))
        print("=")

    def display_result(self):
        logger.debug("result = %s", self.result)
        print(f"MyCashFlow: {self.result}")

    # -------------------- Додавання --------------------
    def add_transaction(self):
        self.result = "Введіть назву танзакції"
        # self.show()
        group = input(">>>> ")

        if self.current_transaction:
            new_transaction = self.manager.add_transaction(parent=self.current_transaction, group=group)
            # self.current_transaction.children.append(new_transaction)
            # self.manager.update_transaction(self.current_transaction)
        else:
            new_transaction = self.manager.add_transaction(parent=None, group=group)

        self.current_transaction = new_transaction

        self.result = f"Транзакція '{new_transaction.group}' додана"
        self.show()

    def _get_max_deep_tree(self, transaction: Transaction, deep:int = 0):

        if len(transaction.entries) > 0 or len(transaction.children) > 0:
            deep += 1

        deep_child = []
        for child in transaction.children:
            deep_child.append(self._get_max_deep_tree(transaction=child, deep=deep))

        if deep_child:
            deep = max(deep_child)

        return deep

    def _build_tree(self, transaction: Transaction, deep: int, prefix_parts: str = None, is_last=True):
        result: str = ""

        if prefix_parts is None:
            prefix_parts = []

        # будуємо prefix
        prefix = ""
        for is_last_parent in prefix_parts:
            prefix += "   " if is_last_parent else "│  "

        # connector для поточного елемента
        connector = "└─" if is_last else "├─"

        tree = f"{prefix}{connector}[T] {transaction.id:06d}"
        result += f"{tree:<{deep}} {transaction.group}: {transaction.total}\n"

        # додаємо інформацію про поточний рівень
        new_prefix_parts = prefix_parts + [is_last]

        items = []
        # entries
        for e in transaction.entries:
            items.append(("entry", e))

        # children
        for c in transaction.children:
            items.append(("transaction", c))

        for i, (item_type, item) in enumerate(items):
            is_last_item = i == len(items) - 1

            child_prefix = ""
            for is_last_parent in new_prefix_parts:
                child_prefix += "   " if is_last_parent else "│  "

            connector = "└─" if is_last_item else "├─"

            child_tree = f"{child_prefix}{connector}[e] {item.id:06d}"

            if item_type == "entry":
                result += f"{child_tree:<{deep}} {item.account}: {item.amount}\n"
            else:
                result += self._build_tree(transaction=item, deep=deep, prefix_parts=new_prefix_parts, is_last=is_last_item)

        return result

    def back_to_parent_transaction(self):
        self.result = "Повертаємось назад"

    def show(self):
        logger.debug("show")
        self.clear_screen()
        self.display_current_transaction()
        self.display_result()

    def greeting(self):
        logger.debug("Greeting")
        self.result = "Welcome!!!"
        self.show()

    def exit(self):
        logger.debug("Good Bye")
        self.result = "Good Bye!!!"
        self.show()
        exit()

    def run(self):
        logger.debug("Run console")
        self.greeting()
        while True:
            logger.debug('--- while ---')

            choice = input(">>>> ")
            logger.debug("choice = %s", choice)

            match choice.lower():
                case "exit":
                    logger.debug("case exit")
                    self.exit()
                case "add":
                    logger.debug("case add")
                    self.add_transaction()
                case "0":
                    logger.debug("case 0 (back)")

                case _:
                    logger.debug("case _")
                    self.result = "Невірний вибір"

            self.show()
