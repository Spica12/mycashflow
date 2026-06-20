from sqlalchemy import (ForeignKey, Integer, String,
                        func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user import User


class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id"), nullable=False
    )
    user: Mapped[User] = relationship("User", backref="tokens")
