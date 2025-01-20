from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from . import schemas
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status

SECRET_KEY = "ff8202b3c6b22e7f0eb4de4a86545070c1079984ebb8d8c4650b3862209d70e9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_tokken(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return schemas.TokenData(email=email)

    except JWTError as e:
        raise credentials_exception