from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db

def db_dep() -> Session:
    return next(get_db())
