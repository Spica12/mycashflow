from sqlalchemy.ext.asyncio import AsyncSession

from src.models.currency import Currency
from src.repositories.currency import CurrencyRepo
from src.schemas.currency import CurrencyCreate, CurrencyUpdate


class CurrencyService:

    async def get_currency_by_code(self, code: str, user_id: str, db: AsyncSession) -> Currency:
        currency: Currency = await CurrencyRepo(db).get_currency_by_code(code, user_id)
        return currency

    async def get_all_currencies(self, user_id: str, db: AsyncSession) -> list[Currency] | None:
        currencies = await CurrencyRepo(db).get_all_currencies(user_id)
        return currencies

    async def add_currency(self, body: CurrencyCreate, user_id: str, db: AsyncSession) -> Currency:
        # Перевіряємо чи існують вже у користувача валюти
        currencies: list[Currency] = await self.get_all_currencies(user_id, db)
        if not currencies:
            # Якщо валют немає — створюємо з прапорцем is_main=True
            new_currency = await CurrencyRepo(db).add_currency(body, user_id, is_main=True)
        else:
            # Якщо вже є — створюємо звичайну другорядну (is_main=False)
            new_currency = await CurrencyRepo(db).add_currency(body, user_id)

        return new_currency

    async def edit_currency(self, code: str, body: CurrencyUpdate, user_id: str ,db: AsyncSession) -> Currency | None:
        edited_currency: Currency = await CurrencyRepo(db).edit_currency(code, body, user_id)
        return edited_currency

    async def delete_currency(self, id: str, user_id: str, db: AsyncSession) -> bool:
        """Сервісний метод для видалення валюти"""
        return await CurrencyRepo(db).delete_currency(id, user_id)



currency_service = CurrencyService()
