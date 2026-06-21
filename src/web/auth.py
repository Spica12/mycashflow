from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.templates import templates
from src.dependencies.db import get_db
from src.models.user import User
from src.services.dependencies import get_current_user_from_cookie
from src.services.auth import auth_service

router_web_auth = APIRouter(tags=["Frontend Auth"])
get_refresh_token = HTTPBearer()


@router_web_auth.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@router_web_auth.get("/login", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

# У вашому router_web_auth
@router_web_auth.get("/logout")
async def web_logout(
    request: Request,
    current_user = Depends(get_current_user_from_cookie),
    db: AsyncSession = Depends(get_db)
):
    """Браузерний маршрут: видаляє дані з БД, стирає куку та перенаправляє на головну"""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    if current_user:
        # Видаляємо токен з бази даних
        await auth_service.logout(current_user, db)

    # Видаляємо куку доступу
    response.delete_cookie(key="access_token", path="/")
    return response
