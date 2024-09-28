from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import models, database
from app.repo.user_repo import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcyNzUxODA3NH0.zhMsm3J39wHzH5rQDhFfAPQq-Vds69sC9zGm4vaSFss"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    """
    Create a new session object.

    This function get the connection with the database and
    create the session.

    Yields:
        [Session]: Object of sqlalchemy Session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(
        data: dict, 
        expires_delta: timedelta = None
    ):
    """Creating access token

    Args:
        data (dict)
        expires_delta (timedelta, optional): time for expiry.

    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ):
    """get current logged in user

    Args:
        token (str, optional): jwt token
        db (Session, optional): session object.

    Raises:
        credentials_exception

    Returns:
        User: Current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user: models.User = Depends(get_current_user)
    ):
    """get current active user

    Args:
        current_user (models.User): currrent user
    Returns:
        User: current_user
    """
    return current_user
