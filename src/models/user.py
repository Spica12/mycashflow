import uuid
from datetime import date
from sqlalchemy import String, Boolean, Date, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base  # Переконіться, що шлях до вашого класу Base правильний


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User email={self.email} is_active={self.is_active}>"
