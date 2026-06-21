
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.config.templates import templates
from src.services.dependencies import get_current_user_from_cookie

router_web_main = APIRouter(tags=["Frontend General"])

@router_web_main.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    current_user = Depends(get_current_user_from_cookie)
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": current_user,
        }
    )
