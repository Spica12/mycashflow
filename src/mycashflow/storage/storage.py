import json

from pathlib import Path
from typing import Any

from mycashflow.logging.logger import logger
from mycashflow.models.transaction import Transaction

# корінь проєкту
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

class JSONStorage:
    def __init__(self, filename: str):
        logger.debug('Init JSONStorage')
        self.filepath = DATA_DIR / filename
        self.filepath.parent.mkdir(exist_ok=True)
        if not self.filepath.exists():
            logger.debug("save empty list")
            self.save([])

    def load_transaction(self, id: int):
        logger.debug('JSONStorage load transaction id=%i', id)

        if not self.filepath.exists():
            logger.warning("%s не існує, повертаю порожній список", self.filepath)
            return []
        try:
            if self.filepath.stat().st_size == 0:  # файл порожній
                logger.warning("%s порожній, повертаю порожній список", self.filepath)
                return []
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if item.get("id") == id:
                        return item
                return None

        except json.JSONDecodeError as e:
            logger.error("Помилка декодування JSON: %s", e)
            return []

    # def load(self) -> list:
    #     logger.debug('Load JSONStorage data')

    #     if not self.filepath.exists():
    #         logger.warning("%s не існує, повертаю порожній список", self.filepath)
    #         return []
    #     try:
    #         if self.filepath.stat().st_size == 0:  # файл порожній
    #             logger.warning("%s порожній, повертаю порожній список", self.filepath)
    #             return []
    #         with open(self.filepath, "r", encoding="utf-8") as f:
    #             return json.load(f)

    #     except json.JSONDecodeError as e:
    #         logger.error("Помилка декодування JSON: %s", e)
    #         return []

    # def save(self, data: list):
    #     logger.debug('Save JSONStorage data')
    #     with open(self.filepath, "w", encoding="utf-8") as f:
    #         json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, item:dict):
        logger.debug('Add JSONStorage data')
        data = self.load()
        if "id" not in item:
            item["id"] = len(data) + 1  # простий авто-ID
        data.append(item)
        self.save(data)
        logger.debug('Success save JSONStorage data')

    def add_transaction(self, transaction: Transaction):
        logger.debug("Add Transaction to JSONStorage: %s", transaction.group)
        item = {
            "id": transaction.id,  # JSONStorage додасть, якщо None
            "group": transaction.group,
            "entries": [{"account": e.account, "amount": e.amount} for e in transaction.entries],
            "total": transaction.total
        }
        self.add(item)
