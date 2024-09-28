from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcyNzUxODA3NH0.zhMsm3J39wHzH5rQDhFfAPQq-Vds69sC9zGm4vaSFss"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """get password hash

    Args:
        password (str): user password

    Returns:
        str: hash value of password
    """
    return pwd_context.hash(password)

def verify_password(
        plain_password: str, 
        hashed_password: str
    ):
    """Password Verification

    Args:
        plain_password (str)
        hashed_password (str)
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """ Generating the access token

    Args:
        data (dict): User data

    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
