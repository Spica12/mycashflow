from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_db
from src.config.templates import templates
from src.models.currency import Currency
from src.services.currency import currency_service
from src.services.dependencies import get_current_user_from_cookie


router_web_currencies = APIRouter(tags=["Frontend Currency Pages"])

@router_web_currencies.get("/", response_class=HTMLResponse)
async def currencies_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_cookie)
):
    # Якщо нема юзера, то перенаправляємо на головну сторінку/
    if not current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    # Отримуємо список усіх валют для відображення в таблиці
    currencies_list = await currency_service.get_all_currencies(current_user.id, db)

    return templates.TemplateResponse(
        request=request,
        name="currencies.html",
        context={"currencies": currencies_list, "user": current_user}
    )

@router_web_currencies.get("/add", response_class=HTMLResponse)
async def add_currency_page(
    request: Request,
    current_user = Depends(get_current_user_from_cookie),
    db: AsyncSession = Depends(get_db),
):
    # Захист: якщо користувач не авторизований — повертаємо на головну
    if not current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    # Отримуємо список усіх валют для відображення в таблиці щоб відображати чи ні на сторінки поле для курсу
    currencies_list = await currency_service.get_all_currencies(current_user.id, db)

    if currencies_list:
        is_main=False
    else:
        is_main=True


    return templates.TemplateResponse(
        request=request,
        name="currency_add.html",
        context={
            "user": current_user,
            "is_main": is_main
        }
    )

@router_web_currencies.get("/edit/{currency_code}", response_class=HTMLResponse)
async def edit_currency_page(
    currency_code: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_cookie)
):
    # 1. Захист: якщо користувач не авторизований — повертаємо на головну
    if not current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    currency = await currency_service.get_currency_by_code(currency_code, current_user.id, db)

    # 3. Якщо такої валюти немає в природі — віддаємо 404 сторінку
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Валюту не знайдено")

    return templates.TemplateResponse(
        request=request,
        name="currency_edit.html",
        context={"user": current_user, "currency": currency}
    )
