from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.currency import Currency
from src.schemas.currency import CurrencyCreate, CurrencyUpdate

class CurrencyRepo:

    def __init__(self, db):
        self.db: AsyncSession = db

    async def get_currency_by_id(self, id: str) -> Currency:
        stmt = select(Currency).filter_by(id=id.upper())
        result = await self.db.execute(stmt)
        currency = result.scalar_one_or_none()
        return currency

    async def add_currency(self, body: CurrencyCreate) -> Currency:
        """Додає нову валюту в базу даних PostgreSQL"""
        new_currency = Currency(**body.model_dump())
        self.db.add(new_currency)
        await self.db.commit()
        await self.db.refresh(new_currency)
        return new_currency

    async def edit_currency(self, id: str, body: CurrencyUpdate) -> Currency | None:
        currency: Currency = await self.get_currency_by_id(id)

        if not currency:
            return None  # Повертаємо None, щоб сервіс/роутер міг повернути красиву 404 помилку

        currency.name = body.name
        currency.rate = body.rate
        currency.is_main = body.is_main
        await self.db.commit()
        await self.db.refresh(currency)
        return currency

    async def delete_currency(self, id: str) -> bool:
        """
        Видаляє валюту за її ISO кодом.
        Повертає True у разі успіху, або False, якщо валюту не знайдено.
        """
        currency = await self.get_currency_by_id(id)
        if not currency:
            return False

        await self.db.delete(currency)
        await self.db.commit()
        return True
