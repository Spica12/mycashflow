from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.settings import settings
from src.dependencies.db import check_db_connection
from src.middleware.logging import log_requests
from src.routers.auth import router_api_auth
from src.utils.logging import logger
from src.web.main import router_web_main
from src.web.auth import router_web_auth


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
app.include_router(router_web_main)
app.include_router(router_web_auth, prefix="/auth")
app.include_router(router_api_auth, prefix="/api")
