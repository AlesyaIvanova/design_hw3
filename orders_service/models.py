from sqlalchemy import Boolean, Table, Column, ForeignKey, Integer, String, MetaData
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    orders = relationship("Order", back_populates="owner")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_username = Column(String, ForeignKey("users.username"))
    price = Column(Integer)
    status = Column(String)

    owner = relationship("User", back_populates="orders")