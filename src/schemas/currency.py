from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class CurrencyBase(BaseModel):
    name: str = Field(..., max_length=50, description="Назва валюти")
    rate: Decimal = Field(Decimal("1.0000"), max_digits=10, decimal_places=4, description="Курс валюти")
    is_main: bool = Field(False, description="Чи є валюта основною")


class CurrencyCreate(CurrencyBase):
    id: str = Field(..., min_length=3, max_length=3, description="ISO код (наприклад: USD)")

    @field_validator("id")
    @classmethod
    def uppercase_id(cls, v: str) -> str:
        return v.upper()


class CurrencyUpdate(CurrencyBase):
    pass  # При редагуванні код ID (наприклад, USD) змінити не можна, тільки назву чи курс


class CurrencyResponse(CurrencyBase):
    id: str

    class Config:
        from_attributes = True
