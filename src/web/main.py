
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.config.templates import templates

router_web_main = APIRouter(tags=["Frontend General"])

@router_web_main.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
