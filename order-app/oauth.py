from fastapi import Depends, HTTPException, status
from . import JWTtokken
from .models import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .schemas import TokenData
from .database import Session,engine


session = Session(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = JWTtokken.verify_tokken(token, credentials_exception)

    
    print(f"Decoded token data: {token_data}")

    
    user = session.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise credentials_exception  
    return user

