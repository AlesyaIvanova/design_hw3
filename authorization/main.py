#from fastapi import FastAPI
#import uvicorn
#import time

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, model, schema
from database import SessionLocal, engine
import uvicorn
import time

from datetime import datetime, timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


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

# @app.post("/user")
# def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     crud.create_user(db=db, user=user)
#     return {"status" : "ok"} 

# @app.get("/user/{username}", response_model=schema.User)
# def read_user(username: str, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=username)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.put("/user")
# def update_user(user: schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user = crud.update_user(db, user, db_user)
#     return {"status" : "ok"}

# @app.delete("/user/{username}")
# def delete_user(username: str, db: Session = Depends(get_db)): 
#     if crud.delete_user(db=db, username=username):
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"status" : "ok"}


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user



if __name__ == "__main__":

    time.sleep(5)
    (model.metadata_obj).create_all(engine)

    uvicorn.run(app, host="0.0.0.0", port=8000)
