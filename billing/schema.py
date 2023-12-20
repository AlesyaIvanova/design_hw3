from pydantic import BaseModel


class User(BaseModel):
    username: str
    balance: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None