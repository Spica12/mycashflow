from sqlalchemy.ext.asyncio import AsyncSession

from src.models.currency import Currency
from src.repositories.currency import CurrencyRepo
from src.schemas.currency import CurrencyCreate, CurrencyUpdate


class CurrencyService:

    async def get_currency_by_id(self, id: str, db: AsyncSession) -> Currency:
        currency: Currency = await CurrencyRepo(db).get_currency_by_id(id)
        return currency

    async def add_currency(self, body: CurrencyCreate, db: AsyncSession) -> Currency:
        new_currency = await CurrencyRepo(db).add_currency(body)
        return new_currency

    async def edit_currency(self, id: str, body: CurrencyUpdate, db: AsyncSession) -> Currency | None:
        edited_currency: Currency = await CurrencyRepo(db).edit_currency(id, body)
        return edited_currency

    async def delete_currency(self, id: str, db: AsyncSession) -> bool:
        """Сервісний метод для видалення валюти"""
        return await CurrencyRepo(db).delete_currency(id)



currency_service = CurrencyService()
