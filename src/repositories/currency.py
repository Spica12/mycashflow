from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.currency import Currency
from src.schemas.currency import CurrencyCreate, CurrencyUpdate
from src.utils.logging import logger

class CurrencyRepo:

    def __init__(self, db):
        self.db: AsyncSession = db

    async def get_currency_by_code(self, code: str, user_id: str) -> Currency | None:
        """Шукає приватну валюту користувача за трилітерним кодом (наприклад, USD)"""
        stmt = select(Currency).filter_by(code=code.upper(), user_id=user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_currencies(self, user_id: str):
        """Повертає список усіх валют із бази даних"""
        stmt = select(Currency).filter_by(user_id=user_id).order_by(Currency.id)
        result = await self.db.execute(stmt)
        currencies = result.scalars().all()
        return currencies

    async def add_currency(self, body: CurrencyCreate, user_id: str, is_main: bool = False) -> Currency:
        """Додає нову валюту в базу даних PostgreSQL"""
        # Якщо валюта головна — її курс примусово 1.0000, інакше — беремо з форми
        rate = Decimal("1.0000") if is_main else body.rate
        new_currency = Currency(
            code=body.code.upper(),
            name=body.name,
            rate=rate,
            is_main=is_main,
            user_id=user_id
        )
        self.db.add(new_currency)
        await self.db.commit()
        await self.db.refresh(new_currency)
        return new_currency

    async def edit_currency(self, code: str, body: CurrencyUpdate, user_id: str) -> Currency | None:
        currency: Currency = await self.get_currency_by_code(code, user_id)

        if not currency:
            logger.debug("Not currency found")
            return None  # Повертаємо None, щоб сервіс/роутер міг повернути красиву 404 помилку

        currency.name = body.name
        currency.rate = body.rate
        await self.db.commit()
        await self.db.refresh(currency)
        return currency

    async def delete_currency(self, code: str, user_id: str) -> bool:
        """
        Видаляє валюту за її ISO кодом.
        Повертає True у разі успіху, або False, якщо валюту не знайдено.
        """
        currency = await self.get_currency_by_code(code, user_id)
        if not currency:
            return False

        await self.db.delete(currency)
        await self.db.commit()
        return True
