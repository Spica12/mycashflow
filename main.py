from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.config.settings import settings
from src.dependencies.db import check_db_connection
from src.middleware.logging import log_requests
from src.utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("MyCashFlow started")
    logger.info("base_dir: %s", settings.BASE_DIR)
    logger.info("db_url: %s", settings.db.DB_HOST)
    await check_db_connection()
    yield
    logger.info("MyCashFlow stopped")


app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_requests)

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
