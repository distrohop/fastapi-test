from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import database
import models
import crud
import schemas

models.Base.metadata.create_all(bind=database.engine)

myApp = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@myApp.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)


@myApp.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail='User not found')
    return db_user


@myApp.post('/users/{user_id}/items', response_model=schemas.Item)
def create_item_for_user(user_id:int, item:schemas.ItemCreate, db: Session= Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@myApp.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@myApp.get('/')
def base_url():
    return {'Hello': 'FastAPI'}
