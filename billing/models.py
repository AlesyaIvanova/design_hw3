from sqlalchemy import Boolean, Table, Column, ForeignKey, Integer, String, MetaData
from database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    balance = Column(Integer)