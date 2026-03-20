from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage

transactions = JSONStorage("transactions.json")
transactions.add({
    "group": "Відпочинок у Карпатах",
    "entries": [
        {"account": "Бензин", "amount": 3000},
        {"account": "Проживання", "amount": 5000}
    ]
})

print(transactions.load())
