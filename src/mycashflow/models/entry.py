from dataclasses import dataclass

@dataclass
class Entry:

    id: int
    parent_id: int
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
            "parent_id": self.parent_id,
            "account": self.account,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        return cls(
            id=data["id"],
            parent_id=data["parent_id"],
            account=data["account"],
            amount=data["amount"]
        )
