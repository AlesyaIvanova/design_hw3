from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud, models, schema
from schema import *
from crud import *
from database import SessionLocal, engine
import uvicorn
import time

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health/")
async def root():
    return {"status": "ok"}


@app.post("/user")
async def create_user(token: str, db: Session = Depends(get_db)):
    response = requests.get('http://authorization:8008/verify?token=' + token)
    response.raise_for_status()
    username = response.content
    db_user = crud.get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, username=username)
    return {"status" : "ok"} 


@app.put("/put_money")
def put_money(token: str, money: int, db: Session = Depends(get_db)):
    response = requests.get('http://authorization:8008/verify?token=' + token)
    response.raise_for_status()
    username = response.content
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.put_money(db, username, money)
    return {"status" : "ok"} 


@app.put("/withdraw_money")
def put_money(token: str, money: int, db: Session = Depends(get_db)):
    response = requests.get('http://authorization:8008/verify?token=' + token)
    response.raise_for_status()
    username = response.content
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.withdraw_money(db, username, money)
    return {"status" : "ok"}


@app.get("/check_balance")
def check_balance(token: str, db: Session = Depends(get_db)):
    response = requests.get('http://authorization:8008/verify?token=' + token)
    response.raise_for_status()
    username = response.content
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.check_balance(db, username)


if __name__ == "__main__":

    time.sleep(30)
    models.Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=8001)