from typing import List, Optional

from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage
from mycashflow.models.entry import Entry


class EntryManager:

    def __init__(self):
        self.storage = JSONStorage("transactions.json")

    # -------------------- Entry --------------------
    def get_entry(self, transaction_id: int, entry_id: int) -> Optional[Entry]:
        t = self.get_by_id(transaction_id)
        if not t:
            return None
        for e in t.entries:
            if e.id == entry_id:
                return e
        return None

    def add_entry(self, transaction_id: int, account: str, amount: float) -> Optional[Entry]:
        t = self.get_by_id(transaction_id)
        if not t:
            return None
        self.last_entry_id += 1
        entry = Entry(id=self.last_entry_id, account=account, amount=amount)
        t.entries.append(entry)
        self.save()
        logger.debug(f"Added entry {entry.id} to transaction {transaction_id}")
        return entry

    def update_entry(self, transaction_id: int, entry_id: int, account: Optional[str] = None, amount: Optional[float] = None) -> bool:
        e = self.get_entry(transaction_id, entry_id)
        if not e:
            return False
        if account:
            e.account = account
        if amount is not None:
            e.amount = amount
        self.save()
        logger.debug(f"Updated entry {entry_id} in transaction {transaction_id}")
        return True

    def delete_entry(self, transaction_id: int, entry_id: int) -> bool:
        t = self.get_by_id(transaction_id)
        if not t:
            return False
        e = self.get_entry(transaction_id, entry_id)
        if not e:
            return False
        t.entries.remove(e)
        self.save()
        logger.debug(f"Deleted entry {entry_id} from transaction {transaction_id}")
        return True

