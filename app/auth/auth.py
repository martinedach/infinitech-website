from datetime import datetime, timedelta
from typing import Optional
from fastapi import Cookie, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from authlib.jose import jwt, JsonWebKey
from app.models.models import User
from app.db.database import get_db
from app.dependencies.utils import get_password_hash
from app.models.pymodels import UserRead  

SECRET_KEY = "YOUR_SECRET_KEY"  # Use a secure and secret key.
ALGORITHM = "HS256"  # Standard symmetric encryption algorithm for JWT.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(username: str, password: str, db: Session):
    print(f"Authenticating user: {username}")  # Debug print
    user = get_user(db, username)
    if not user:
        print(f"User '{username}' not found.")  # Debug print
        return False
    print(f"Found user: {user.username}, Hashed Password: {user.hashed_password}")  # Debug print
    if not verify_password(password, user.hashed_password):
        print(f"Password mismatch for user: {username}")  # Debug print
        return False
    print(f"User '{username}' authenticated successfully.")  # Debug print
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    header = {'alg': ALGORITHM}
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes if no duration is provided.
    to_encode.update({"exp": expire})
    token = jwt.encode(header, to_encode, SECRET_KEY)
    return token.decode('utf-8')  # Ensure token is a string for response.





def get_current_user(
    request: Request,
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token:
        raise credentials_exception

    try:
        data = jwt.decode(access_token, SECRET_KEY)
        data.validate()
        username = data.get('sub')
        if not username:
            raise credentials_exception
    except jwt.ExpiredTokenError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    # Use model_validate instead of from_orm
    return UserRead.model_validate(user).model_dump()