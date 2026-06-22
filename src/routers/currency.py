from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_db
from src.models.currency import Currency
from src.schemas.currency import CurrencyCreate, CurrencyUpdate, CurrencyResponse

router_api_currencies = APIRouter(prefix="/currencies", tags=["Currencies API"])


# @router_api_currencies.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
# async def create_currency(body: CurrencyCreate, db: AsyncSession = Depends(get_db)):
#     # Перевіряємо, чи немає вже такої валюти
#     stmt = select(Currency).filter_by(id=body.id)
#     res = await db.execute(stmt)
#     if res.scalar_one_or_none():
#         raise HTTPException(status_code=409, detail=f"Валюта {body.id} вже існує")

#     # Якщо нова валюта стає основною, знімаємо прапорець з інших
#     if body.is_main:
#         await db.execute(select(Currency).filter_by(is_main=True))  # логіку скидання можна розширити

#     new_currency = Currency(**body.model_dump())
#     db.add(new_currency)
#     await db.commit()
#     await db.refresh(new_currency)
#     return new_currency


# @router_api_currencies.put("/{currency_id}", response_model=CurrencyResponse)
# async def update_currency(currency_id: str, body: CurrencyUpdate, db: AsyncSession = Depends(get_db)):
#     stmt = select(Currency).filter_by(id=currency_id.upper())
#     res = await db.execute(stmt)
#     currency = res.scalar_one_or_none()

#     if not currency:
#         raise HTTPException(status_code=404, detail="Валюту не знайдено")

#     currency.name = body.name
#     currency.rate = body.rate
#     currency.is_main = body.is_main

#     await db.commit()
#     await db.refresh(currency)
#     return currency
