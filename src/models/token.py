import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user import User


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Збільшуємо довжину до 512, щоб JWT-токен точно помістився
    token: Mapped[str] = mapped_column(String(512), nullable=True, index=True)

    # Використовуємо правильний UUID тип для ForeignKey
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),  # CASCADE видалить токени, якщо видалити юзера
        nullable=False
    )

    # Сучасний зв'язок 2.0 (back_populates або backref)
    user: Mapped["User"] = relationship("User", backref="tokens")
