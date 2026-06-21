from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.templates import templates
from src.dependencies.db import get_db
from src.models.user import User

router_web_auth = APIRouter(tags=["Frontend Auth"])
get_refresh_token = HTTPBearer()


@router_web_auth.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )
