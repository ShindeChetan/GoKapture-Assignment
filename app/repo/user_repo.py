from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User
from app.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    """Get user form username

    Args:
        db (Session)
        username (str)

    Returns:
        User : User object
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    """Creating the new user

    Args:
        db (Session)
        user (UserCreate)

    Returns:
        User : User object
    """
    db_user = User(username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authnticate the user

    Args:
        db (Session)
        username (str)
        password (str)

    Returns:
        User : User object
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user
