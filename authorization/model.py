from sqlalchemy import Boolean, Table, Column, ForeignKey, Integer, String, MetaData
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)


metadata_obj = MetaData()
users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String(16), nullable=False, unique=True, index=True),
    Column("hashed_password", String(30), nullable=False),
    Column("first_name", String(30), nullable=False),
    Column("last_name", String(30), nullable=False),
    Column("email", String(60), nullable=False),
    Column("phone", String(60), nullable=False)
)