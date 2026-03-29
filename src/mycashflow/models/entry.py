
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


@dataclass
class Entry:

    id: int
    parent_id: int
    parent: "Transaction"

    account: str
    amount: int

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

    def __str__(self) -> int:
        return str(f"{self.id:06d} - {self.account}: {self.amount}")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": 'entry',
            "parent_id": self.parent.id,
            "account": self.account,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        if data["type"] == "entry":
            return cls(
                id=data["id"],
                parent_id=data["parent_id"],
                account=data["account"],
                amount=data["amount"]
            )
