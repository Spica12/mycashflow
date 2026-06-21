from fastapi.templating import Jinja2Templates
from src.config.settings import settings


templates = Jinja2Templates(directory=settings.BASE_DIR / "templates")
