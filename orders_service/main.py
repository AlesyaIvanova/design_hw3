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
    username = verify_user(token)
    db_user = crud.get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, username=username)
    return {"status" : "ok"} 


@app.post("/user/{token}/order")
def create_order_for_user(token: str, order: OrderCreate, db: Session = Depends(get_db)):
    username = verify_user(token)
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.create_user_order(db=db, token=token, username=username, order=order)
    return {"status" : "ok"}


@app.get("/orders/{token}", response_model=list[schema.Order])
def read_orders(token: str, db: Session = Depends(get_db)):
    username = verify_user(token)
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    orders = crud.get_users_orders(db=db, username=username)
    return orders


if __name__ == "__main__":

    time.sleep(30)
    models.Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=8002)
