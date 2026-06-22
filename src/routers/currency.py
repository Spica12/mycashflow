from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_db
from src.models.currency import Currency
from src.services.currency import currency_service

from src.schemas.currency import CurrencyCreate, CurrencyUpdate, CurrencyResponse

router_api_currencies = APIRouter(prefix="/currencies", tags=["Currencies API"])


@router_api_currencies.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
async def create_currency(body: CurrencyCreate, db: AsyncSession = Depends(get_db)):

    # Перевіряємо, чи немає вже такої валюти
    currency: Currency = await currency_service.get_currency_by_id(body.id, db)
    if currency:
        raise HTTPException(status_code=409, detail=f"Валюта {body.id} вже існує")

    new_currency = await currency_service.add_currency(body, db)

    return new_currency


@router_api_currencies.put("/{currency_id}", response_model=CurrencyResponse)
async def update_currency(currency_id: str, body: CurrencyUpdate, db: AsyncSession = Depends(get_db)):

    edited_currency: Currency = await currency_service.edit_currency(currency_id, body, db)

    if not edited_currency:
        raise HTTPException(status_code=404, detail="Валюту не знайдено")

    return edited_currency

@router_api_currencies.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: str, db: AsyncSession = Depends(get_db)):
    """Ендпоінт для видалення другорядної валюти."""
    # 1. Перевіряємо, чи існує валюта
    currency = await currency_service.get_currency_by_id(currency_id, db)
    if not currency:
        raise HTTPException(status_code=404, detail="Валюту не знайдено")

    # 2. Забороняємо видалення, якщо вона є головною
    if currency.is_main:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неможливо видалити основну валюту системи. Спочатку призначте іншу валюту головною."
        )

    # 3. Видаляємо сутність
    try:
        await currency_service.delete_currency(currency_id, db)
    except Exception:
        # Спрацює RESTRICT захист, якщо до валюти вже прив'язані реальні рахунки
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неможливо видалити валюту, оскільки до неї прив'язані чинні рахунки."
        )

    return None
