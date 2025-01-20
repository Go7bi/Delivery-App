
from fastapi import APIRouter, status, Depends, HTTPException
from  .schemas import SignUpModel,LoginUser
from  .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from .database import Session,engine
from fastapi.security import OAuth2PasswordRequestForm
from .import JWTtokken

singn_router = APIRouter(
    
    tags=['Authentication']
)
session = Session(bind = engine)

@singn_router.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):

    user=session.query(User).filter(User.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credential')
    if not check_password_hash(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')
    

    access_token = JWTtokken.create_access_token(
        data={"sub": user.email}
    )
    return {'access_token':access_token, 'token_type':"bearer"}