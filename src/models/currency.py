import uuid
from decimal import Decimal
from sqlalchemy import String, Numeric, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user import User


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Використовуємо міжнародний трилітерний код як ID (наприклад: UAH, USD, EUR)
    code: Mapped[str] = mapped_column(String(3), nullable=False)

    # Назва валюти (наприклад: Українська гривня, Долар США)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Курс відносно основної валюти.
    # precision=10, scale=4 дозволяє зберігати курси на кшталт 40.2500 або 0.0245
    rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("1.0000"), nullable=False)

    # Прапорець, який вказує, чи є ця валюта базовою для всієї системи (чи зводити до неї баланс)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped[User] = relationship("User", backref="currencies")

    # Код валюти має бути унікальним тільки для конкретного user_id!
    __table_args__ = (
        UniqueConstraint("code", "user_id", name="uq_currency_code_per_user"),
    )
    def __repr__(self) -> str:
        return f"<Currency {self.id}: rate={self.rate} is_main={self.is_main}>"
