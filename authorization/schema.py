from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    # first_name: str
    # last_name: str
    # email: str
    # phone: str


class User(UserBase):
    # first_name: str
    # last_name: str
    # email: str
    # phone: str

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None