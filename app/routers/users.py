from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.schemas import UserCreate, UserOut
from app.repo.user_repo import get_user_by_username, create_user, authenticate_user
from app.dependencies import get_db, create_access_token


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/api/register", response_model=UserOut)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
    ):
    """Register user endpoint"""
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hashibg the password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    
    return create_user(db=db, user=user)

@router.post("/api/login")
def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
    ):
    """User login endpoint"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
