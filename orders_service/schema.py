from pydantic import BaseModel


class OrderBase(BaseModel):
    title: str
    description: str | None = None
    price: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    owner_username: str
    status: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    orders: list[Order] = []

    class Config:
        orm_mode = True