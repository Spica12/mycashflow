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
        self.load()
        # if not self.filepath.exists():
        #     logger.debug("save empty dict")
        #     self.data = self.get_empty_data()
        #     self.save(self.data)

    def create_empty_data(self) -> None:
        self.data =  {
            "current_id": 0,
            "items": {},
        }
        self.save()

    def load(self) -> None:
        logger.debug('Load JSONStorage data')

        if not self.filepath.exists():
            logger.warning("%s не існує, повертаю порожній словник", self.filepath)
            self.create_empty_data()
            # return {}
        try:
            if self.filepath.stat().st_size == 0:  # файл порожній
                logger.warning("%s порожній, повертаю порожній словник", self.filepath)
                self.create_empty_data()
                # return {}
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                # return json.load(f)

        except json.JSONDecodeError as e:
            logger.error("Помилка декодування JSON: %s", e)
            self.create_empty_data()
            # return {}

        logger.debug('Load JSONStorage data finish')

    def save(self):
        logger.debug('Save JSONStorage data')
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_current_id(self) -> int:
        return self.data.get("current_id")

    def increment_id(self):
        self.data["current_id"] += 1
        self.save()

    def get_item_data_by_id(self, id: int) -> dict | None:
        logger.debug('Get item data by id = %i', id)
        logger.debug(type(self.data))

        items: dict = self.data.get("items")
        # logger.debug("items = %s", items)

        return self.data["items"].get(str(id), None)

    def add_item_data(self, item_data: dict) -> dict:
        current_id = item_data["id"]
        # Зберігаємо транзакцію в словник json
        self.data["current_id"] = current_id
        self.data["items"][str(current_id)] = item_data
        self.save()

        return self.get_item_data_by_id(current_id)

    def update_item_data(self, item_data: dict) -> None:
        id = item_data["id"]
        self.data["items"][str(id)] = item_data
        self.save()

    def delete_item(self, id: int) -> None:
        self.data["items"].pop([str(id)], None)
        self.save()

    # def add(self, item:dict):
    #     logger.debug('Add JSONStorage data')
    #     data = self.load()
    #     if "id" not in item:
    #         item["id"] = len(data) + 1  # простий авто-ID
    #     data.append(item)
    #     self.save(data)
    #     logger.debug('Success save JSONStorage data')
