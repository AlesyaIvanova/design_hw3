from sqlalchemy.orm import Session
import models, schema
from schema import *
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import requests


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def verify_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    response = requests.get('http://authorization:8008/verify?token=' + token)
    if response.status_code != 200:
        raise credentials_exception
    username = response.json()["username"]
    return username


def create_user(db: Session, username: str):
    db_user = models.User(
        username=username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def withdraw_money_for_order(token: str, price: int):
    response = requests.put('http://billing:8001/withdraw_money?token=' + token + "&money=" + str(price))
    return response.status_code == 200


def create_user_order(db: Session, token: str, username: str, order: OrderCreate):
    price = order.price
    if withdraw_money_for_order(token, price):
        status = "ok"
    else:
        status = "cancelled"
    db_item = models.Order(**order.dict(), owner_username=username, status=status)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    if status == "cancelled":
        raise HTTPException(status_code=402, detail="Not enough money")
    return db_item


def get_users_orders(db: Session, username: str):
    db_user = get_user_by_username(db, username)
    return db_user.orders