from fastapi import (APIRouter, BackgroundTasks, Depends, HTTPException,
                     Request, Security, status, Response)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordRequestForm)
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import messages
from src.config.templates import templates
from src.dependencies.db import get_db
from src.models.user import User
# from src.schemas.users import (RequestPasswordResetSchema, TokenSchema,
#                                UserSchema, UserMyResponseSchema)
from src.schemas.users import UserSchema, CreateUserSchema, UserMyResponseSchema
from src.schemas.token import TokenSchema, RefreshTokenRequestSchema
from src.services.auth import auth_service
from src.services.dependencies import get_current_user_from_cookie

router_api_auth = APIRouter(prefix="/auth", tags=["Auth"])
get_refresh_token = HTTPBearer()

@router_api_auth.post(
    "/register",
    response_model=UserMyResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def register(
    body: UserSchema,
    request: Request,
    bt: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    # need response model and body schema
    exist_user_by_email = await auth_service.get_user_by_email(body.email, db=db)
    if exist_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=messages.EMAIL_IS_ALREADY_BUSY,
        )

    hashed_body = CreateUserSchema(
        email=body.email,
        hashed_password=auth_service.get_password_hash(body.password)
    )
    new_user = await auth_service.create_user(hashed_body, db
    )

    return new_user


@router_api_auth.post("/login", response_model=TokenSchema)
async def login(
    response: Response,  # Додаємо для запису кук
    body: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # 1. Шукаємо користувача за username (це ваш email у формі)
    user = await auth_service.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=messages.ACCOUNT_BLOCKED
        )
    # Якщо у вас є поле підтвердження пошти (опціонально)
    # if not user.confirmed:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)

    # 2. ВИПРАВЛЕНО: міняємо user.password на user.hashed_password
    if not auth_service.verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD
        )

    # 3. ГЕНЕРУЄМО ТОКЕНИ
    access_token = await auth_service.create_access_token(user.email)
    refresh_token = await auth_service.create_refresh_token(user.email)

    await auth_service.update_refresh_token(user, refresh_token, db)

    # 4. ЗАПИСУЄМО В COOKIES (щоб авторизація не злітала на HTML сторінках сайту)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 хвилин
        samesite="lax",
        secure=False   # виставте True на продакшені з HTTPS
    )

    # 5. ПОВЕРТАЄМО JSON (відповідає вашій TokenSchema для Swagger)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router_api_auth.post("/logout", status_code=status.HTTP_200_OK)
async def api_logout(
    response: Response,
    current_user = Depends(get_current_user_from_cookie),
    db: AsyncSession = Depends(get_db)
):
    """Технічний ендпоінт для анулювання сесії в БД та очищення кук"""
    if current_user:
        # 1. Видаляємо Refresh токен з PostgreSQL таблиці tokens
        await auth_service.logout(current_user, db)

    # 2. Видаляємо Access токен з кук браузера
    response.delete_cookie(key="access_token", path="/")

    return {"message": "Сесію успішно завершено"}

@router_api_auth.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    response: Response,
    body: RefreshTokenRequestSchema,
    db: AsyncSession = Depends(get_db)
):
    """Ендпоінт оновлення Access та Refresh токенів за допомогою діючого Refresh токена"""

    # 1. Валідуємо JWT структуру токена та дістаємо email
    email = await auth_service.verify_refresh_token(body.refresh_token)

    # 2. Перевіряємо, чи цей токен фізично існує в PostgreSQL таблиці tokens
    token_record = await auth_service.get_token_record(body.refresh_token, db)
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сесію не знайдено або вона була анульована"
        )

    # 3. Шукаємо користувача, якому належить токен
    user = await auth_service.get_user_by_email(email, db)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувач не знайдений або заблокований"
        )

    # 4. ГЕНЕРУЄМО НОВУ ПАРУ ТОКЕНІВ (Ротація токенів для безпеки)
    new_access_token = await auth_service.create_access_token(user.email)
    new_refresh_token = await auth_service.create_refresh_token(user.email)

    # 5. Оновлюємо Refresh токен у базі даних (замінюємо старий на новий)
    await auth_service.update_refresh_token(user, new_refresh_token, db)

    # 6. Оновлюємо HTTP-Only куку для фронтенду сайту
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        max_age=1800,  # 30 хвилин
        samesite="lax",
        secure=False
    )

    # 7. Повертаємо нові токени для клієнтів API
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

# @router_api_auth.get("/refresh", response_model=TokenSchema)
# async def refresh_token(
#     credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
#     db: AsyncSession = Depends(get_db),
# ):
#     token = credentials.credentials

#     check = await auth_service.check_access_token_blacklist(token, db)
#     if check is not None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_TOKEN
#         )
#     email = await auth_service.get_email_from_token(token)
#     user = await auth_service.get_user_by_email(email, db)
#     refresh_token = await auth_service.get_refresh_token_by_user(user, db)
#     if refresh_token.token != token:
#         await auth_service.update_refresh_token(user, None, db)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=messages.INVALID_REFRESH_TOKEN,
#         )

#     access_token = await auth_service.create_access_token(user.email)
#     refresh_token = await auth_service.create_refresh_token(user.email)
#     await auth_service.update_refresh_token(user, refresh_token, db)

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#     }


# @router_api_auth.get("/password-reset/{token}", response_model=None)
# async def password_reset(
#     token: str,
#     bt: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
# ):
#     email = await auth_service.get_email_from_token(token)
#     user = await auth_service.get_user_by_email(email, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR
#         )
#     new_password = auth_service.generate_password()
#     new_password_hash = auth_service.get_password_hash(new_password)
#     await auth_service.update_password(user.id, new_password_hash, db)
#     bt.add_task(
#         EmailService().send_new_password_mail,
#         user.email,
#         user.username,
#         new_password,
#     )
#     return {"message": messages.NEW_PASSWORD_SENT}


# @router_api_auth.post("/password-reset", response_model=None)
# async def request_password_reset(
#     body: RequestPasswordResetSchema,
#     request: Request,
#     bt: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
# ):
#     # Check if email exists
#     exist_user = await auth_service.get_user_by_email(body.email, db)
#     if exist_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=messages.ACCOUNT_NOT_FOUND
#         )
#     if not exist_user.confirmed:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=messages.EMAIL_NOT_CONFIRMED,
#         )
#     # Check if username is valid
#     if body.username != exist_user.username:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=messages.INVALID_USERNAME
#         )
#     bt.add_task(
#         EmailService().send_request_password_mail,
#         exist_user.email,
#         exist_user.username,
#         str(request.base_url),
#     )
#     return {"message": messages.PASSWORD_RESET_REQUEST_SENT}
