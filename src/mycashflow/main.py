from mycashflow.logging.logger import logger
from mycashflow.storage.storage import JSONStorage
from mycashflow.models.transaction import Transaction

transactions = JSONStorage("transactions.json")

# створюємо транзакцію
t = Transaction(group="Відпочинок у Карпатах")
t.add_entry("Бензин", -3000)
t.add_entry("Проживання", -5000)

logger.info(f"Transaction total: {t.total}")  # -8000

# зберігаємо у JSONStorage
# transactions.add({
#     "id": None,  # JSONStorage автоматично додасть
#     "group": t.group,
#     "entries": [{"account": e.account, "amount": e.amount} for e in t.entries],
#     "total": t.total
# })
transactions.add_transaction(t)


print(transactions.load())
