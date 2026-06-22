from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_db
from src.config.templates import templates
from src.models.currency import Currency
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
    stmt = select(Currency).order_by(Currency.id)
    res = await db.execute(stmt)
    currencies_list = res.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="currencies.html",
        context={"currencies": currencies_list, "user": current_user}
    )
