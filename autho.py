from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta

SECRET_KEY = "95996b91ff95c78fadbf00640e3d9e5ddf83806a3194e4e4a2c74cdb65b954ec"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Database Model (Our table structure)
class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    hashed_pwd = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)

BaseModel.metadata.create_all(bind="engine")

