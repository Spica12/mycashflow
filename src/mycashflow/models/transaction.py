from dataclasses import dataclass, field
from typing import List, Optional

from mycashflow.models.entry import Entry


@dataclass
class Transaction:

    id: int                  # Авто-ID (JSONStorage додасть)
    group: str                     # Назва групи або проекту

    parent_id: Optional[int] = None
    parent: Optional["Transaction"] = None

    entries_id: List[int] = field(default_factory=list)
    children_id: List[int] = field(default_factory=list)

    entries: List[Entry] = field(default_factory=list)
    children: List["Transaction"] = field(default_factory=list)  # дочірні транзакції

    @property
    def total(self) -> float:
        sum_entries = sum((entry.amount) for entry in self.entries)
        sum_children = sum((child.total) for child in self.children)

        return sum_entries + sum_children

    def add_entry(self, id: int, account: str, amount: float):
        self.entries.append(
            Entry(id=id, parent_id=self.id, account=account, amount=amount)
        )


    def __str__(self) -> int:
        output_str: str = f"{self.id:06d} - {self.group}: {self.total}"
        for entry in self.entries:
            output_str += f"\n --> {entry}"

        return output_str

    # id: int                  # Авто-ID (JSONStorage додасть)
    # parent_id: Optional[int]
    # group: str                     # Назва групи або проекту
    # entries: List[Entry] = field(default_factory=list)
    # children: List["Transaction"] = field(default_factory=list)  # дочірні транзакції

    # ----------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": 'transaction',
            "parent_id": self.parent_id,
            "group": self.group,
            "entries_id": self.entries_id,
            "children_id": self.children_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Transaction:
        if data["type"] == "transaction":
            return cls(
                id=data["id"],
                group=data["group"],
                parent_id=data["parent_id"],
                entries_id=data["entries_id"],
                children_id=data["children_id"]
            )
