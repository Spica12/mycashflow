from dataclasses import dataclass, field
from typing import List


@dataclass
class Entry:
    account: str
    amount: float


@dataclass
class Transaction:
    group: str                     # Назва групи або проекту
    entries: List[Entry] = field(default_factory=list)
    id: int = None                 # Авто-ID (JSONStorage додасть)

    @property
    def total(self) -> float:
        return sum(entry.amount for entry in self.entries)

    def add_entry(self, account: str, amount: float):
        self.entries.append(Entry(account=account, amount=amount))
