from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import jwt
from jwt import InvalidTokenError
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlite_db import Users,session

# Configuration
SECRET_KEY = "d1707adc314494aaf074b94c628a94d9d34b6d72f81a86f08ec4611cbe37b486"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class NewUser(BaseModel):
    user_name: str
    password: str

class NewUserResponse(BaseModel):
    status: str
    user_id: int

class LoginUser(BaseModel):
    user_name: str
    password: str

class LoginUserResponse(BaseModel):
    status: str
    user_token: str

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except InvalidTokenError:
        return None


# Utility Functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/new", response_model=NewUserResponse)
async def create_user(user: NewUser):

    username = user.user_name
    hashed = hash_password(password=user.password)

    n_user = Users(username=username,pass_hash=hashed)
    session.add(n_user)
    session.flush()
    id = n_user.id
    session.commit()

    nres = NewUserResponse(status="success",user_id=id)

    return nres

@router.post("/login", response_model=LoginUserResponse)
async def login(user: LoginUser):

    user_info = session.query(Users).filter(Users.username==user.user_name).first()

    # ures = None

    if user_info is not None:
        username = user_info.username
        stored_hash = user_info.pass_hash

        if verify_password(user.password,stored_hash):
            access_token = create_access_token(
                data={"sub": username},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            logres = LoginUserResponse(status="success",user_token=access_token)
            return logres
        else:
            logres = LoginUserResponse(status="fail",user_token="None")
            return logres      
    else:
        logres = LoginUserResponse(status="fail",user_token="None")
        return logres
