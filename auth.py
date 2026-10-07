from fastapi import Depends,FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


client = MongoClient(os.getenv("MONGODB_URI"))
db = client["api_testing"]
metadata_collection = db["users"]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str]
    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    username: str
    email: Optional[str]
    disabled: Optional[bool]

class UserDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_pwd(plain_pwd,hashed_pwd):
    return pwd_context.verify(plain_pwd,hashed_pwd)

def get_pwd_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    user_data = metadata_collection.find_one({"username": username})
    if user_data:
        return UserDB(**user_data) #will give data in key,value pairs
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_pwd(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict,expires_delta:Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15) #What if expires_delta doesn't exist?

    to_encode.update({"exp":expire}) #adds expiration time to token
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) #token created, jwt signed
    return encoded_jwt

async def get_current_user(token:str = Depends(oauth2_scheme)): #Getting the current user from the token
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user:UserDB=Depends(get_current_user)): #Checking if the user is active
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user

@app.post("/register")
async def register_user(user: UserCreate):
    existing_user = metadata_collection.find_one({"username": user.username})

    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    hashed_password = get_pwd_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False
    }
    metadata_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

@app.post("/token",response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data= {"sub":user.username},expires_delta=access_token_expires)
    return {"access_token":access_token,"token_type":"bearer"}