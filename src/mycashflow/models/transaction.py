from dataclasses import dataclass, field
from typing import List, Optional

from mycashflow.models.entry import Entry


@dataclass
class Transaction:

    id: int                  # Авто-ID (JSONStorage додасть)
    parent_id: Optional[int]
    group: str                     # Назва групи або проекту
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

    def _get_max_deep_tree(self, deep:int = 0):

        if len(self.entries) > 0 or len(self.children) > 0:
            deep += 1

        deep_child = []
        for child in self.children:
            deep_child.append(child._get_max_deep_tree(deep=deep))

        if deep_child:
            deep = max(deep_child)

        return deep

    def _build_tree(self, deep: int, prefix_parts: str = None, is_last=True):
        result: str = ""

        if prefix_parts is None:
            prefix_parts = []

        # будуємо prefix
        prefix = ""
        for is_last_parent in prefix_parts:
            prefix += "   " if is_last_parent else "│  "

        # connector для поточного елемента
        connector = "└─" if is_last else "├─"

        tree = f"{prefix}{connector}[T] {self.id:06d}"
        result += f"{tree:<{deep}} {self.group}: {self.total}\n"

        # додаємо інформацію про поточний рівень
        new_prefix_parts = prefix_parts + [is_last]

        items = []
        # entries
        for e in self.entries:
            items.append(("entry", e))

        # children
        for c in self.children:
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
                result += item._build_tree(deep=deep, prefix_parts=new_prefix_parts, is_last=is_last_item)

        return result

    def out_tree(self):

        deep = self._get_max_deep_tree(deep=0) + 1
        deep = 2 + deep * 3 + 7
        return str(self._build_tree(deep=deep))

    def __str__(self) -> int:
        output_str: str = f"{self.id:06d} - {self.group}: {self.total}"
        for entry in self.entries:
            output_str += f"\n --> {entry}"

        return output_str
