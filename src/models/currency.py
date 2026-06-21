from decimal import Decimal
from sqlalchemy import String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Currency(Base):
    __tablename__ = "currencies"

    # Використовуємо міжнародний трилітерний код як ID (наприклад: UAH, USD, EUR)
    id: Mapped[str] = mapped_column(String(3), primary_key=True)

    # Назва валюти (наприклад: Українська гривня, Долар США)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Курс відносно основної валюти.
    # precision=10, scale=4 дозволяє зберігати курси на кшталт 40.2500 або 0.0245
    rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("1.0000"), nullable=False)

    # Прапорець, який вказує, чи є ця валюта базовою для всієї системи (чи зводити до неї баланс)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Currency {self.id}: rate={self.rate} is_main={self.is_main}>"
