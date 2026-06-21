from fastapi import Request, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.dependencies.db import get_db
from src.services.auth import auth_service

async def get_current_user_from_cookie(request: Request, db: AsyncSession = Depends(get_db)):
        """
        Зчитує токен із HTTP-Only Cookies та повертає об'єкт користувача з БД.
        Якщо токен відсутній або недійсний, повертає None (користувач — гість).
        """
        # 1. Дістаємо куку access_token
        token_cookie = request.cookies.get("access_token")
        if not token_cookie:
            return None

        try:
            # 2. Очищаємо префікс Bearer, якщо він є
            if token_cookie.startswith("Bearer "):
                token = token_cookie.split(" ")[1]
            else:
                token = token_cookie

            # 3. Декодуємо JWT токен
            payload = jwt.decode(token, settings.auth.SECRET_KEY_JWT, algorithms=[settings.auth.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None

        except (jwt.JWTError, AttributeError):
            return None

        # 4. Шукаємо користувача в базі даних за його сервісним методом
        user = await auth_service.get_user_by_email(email, db)
        return user
