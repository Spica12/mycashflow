from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    # Автоматично додаємо ці колонки до ВСІХ таблиць, що наслідуються від Base
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @property
    def created_at_local(self) -> datetime:
        """Конвертує час сервера з UTC у локальний час для відображення"""
        if self.created_at.tzinfo is None:
            utc_time = self.created_at.replace(tzinfo=ZoneInfo("UTC"))
        else:
            utc_time = self.created_at
        return utc_time.astimezone(ZoneInfo("Europe/Kyiv"))

    @property
    def updated_at_local(self) -> datetime:
        """Конвертує час оновлення сервера з UTC у локальний час для відображення"""
        if self.updated_at.tzinfo is None:
            utc_time = self.updated_at.replace(tzinfo=ZoneInfo("UTC"))
        else:
            utc_time = self.updated_at
        return utc_time.astimezone(ZoneInfo("Europe/Kyiv"))
