from typing import List, Optional

from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage
from mycashflow.models.transaction import Transaction
from mycashflow.models.entry import Entry


class TransactionManager:

    def __init__(self):
        self.storage = JSONStorage("transactions.json")

    # -------------------- Доступ --------------------
    def save(self):
        """Зберігає всі транзакції у JSON"""
        data = [t.to_dict() for t in self.transactions]
        self.storage.save(data)
        logger.debug(f"Saved {len(self.transactions)} transactions")

    # def get_all(self) -> List[Transaction]:
    #     """Повертає список усіх транзакцій"""
    #     transactions_data = self.storage.load()
    #     # конвертуємо dict → об'єкти Transaction
    #     self.transactions: List[Transaction] = [
    #         Transaction.from_dict(data=d) for d in transactions_data
    #     ]

    #     # Створюємо список транзакцій
    #     for item_data in transactions_data:
    #         if item_data.get("type") == "transaction":
    #             self.transactions.append(Transaction.from_dict(data=item_data))

    #     # Створюємо і додаємо Entry в транзакції
    #     for item_data in transactions_data:
    #         if item_data.get("type") == "entry":
    #             entry: Entry = Entry.from_dict(item_data)
    #             for transaction in self.transactions:
    #                 if entry.parent_id == transaction.id:
    #                     transaction.entries.append(entry)

    #     # Створюємо зв'язки між транзакціями
    #     for transaction in self.transactions:
    #         for child_id in transaction.children_id:
    #             for t in self.transactions:
    #                 if t.id == child_id:
    #                     transaction.children.append(t)

    #     # останні id для генерації
    #     self.last_id = max((item_data.get("id") for item_data in transactions_data), default=0)

    def get_by_id(self, id: int) -> Optional[Transaction | Entry]:
        """Повертає запис за id"""

        # Зчитуємо з пам'яті транзакцію по id
        item_data: dict = self.storage.get_item_data_by_id(id=id)
        logger.debug(item_data)

        if item_data is None:
            return None

        elif item_data["type"] == "transaction":
            del item_data["type"]
            transaction: Transaction = Transaction(**item_data)

            transaction.entries = [self.get_by_id(id=entry_id) for entry_id in transaction.entries_id]
            transaction.children = [self.get_by_id(id=child_id) for child_id in transaction.children_id]

            return transaction

        elif transaction.type == "entry":
            del item_data["type"]
            return Entry(**item_data)

    # -------------------- Створення --------------------


    def add_transaction(self, group: str, parent: Optional[Transaction] = None) -> Transaction:
        """Додає нову транзакцію з унікальним id"""

        # Створюємо нову транзакцію
        current_id = self.storage.get_current_id() + 1

        if parent:
            transaction = Transaction(id=current_id, parent_id=parent.id, group=group, entries=[])
            self.storage.update_item_data(transaction.to_dict())

            parent.children_id.append(transaction.id)
            self.storage.update_item_data(parent.to_dict())
        else:
            transaction = Transaction(id=current_id, parent_id=None, group=group, entries=[])
            self.storage.update_item_data(transaction.to_dict())

        self.storage.increment_id()

        logger.debug(f"Added transaction {transaction.id}")

        return transaction

    # # -------------------- Оновлення --------------------
    # def update_transaction(
    #         self,
    #         transaction: Transaction,
    #     ) -> bool:
    #     """Оновлює назву групи або список Entry"""
    #     t = self.get_by_id(transaction.id)
    #     if not t:
    #         return False

    #     t = transaction
    #     self.save()

    #     logger.debug(f"Updated transaction {transaction}")
    #     return True

    # # -------------------- Видалення --------------------
    # def delete_transaction(self, transaction_id: int) -> bool:
    #     """Видаляє транзакцію за id"""
    #     t = self.get_by_id(transaction_id)
    #     if not t:
    #         return False
    #     self.transactions.remove(t)
    #     self.save()
    #     logger.debug(f"Deleted transaction {transaction_id}")
    #     return True
