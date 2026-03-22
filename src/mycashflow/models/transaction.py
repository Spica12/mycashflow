from dataclasses import dataclass, field
from typing import List


class Entry:

    def __init__(self, account: str, amount: float):
        self.account: str = account
        self._amount = None
        self.amount = amount

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

    def __str__(self) -> int:
        return str(f"{self.account}: {self.amount}")


@dataclass
class Transaction:
    group: str                     # Назва групи або проекту
    entries: List[Entry] = field(default_factory=list)
    id: int = None                 # Авто-ID (JSONStorage додасть)

    @property
    def total(self) -> float:
        return sum((entry.amount * entry.scale) for entry in self.entries)

    def add_entry(self, account: str, amount: float):
        self.entries.append(
            Entry(account=account, amount=amount)
        )

    
