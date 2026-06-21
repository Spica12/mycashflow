from pydantic import BaseModel


class TokenSchema(BaseModel):
    # id: int
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    # created_at: datetime
    # updated_at: datetime

class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str
