from fastapi import APIRouter, status, Depends, HTTPException
from  .schemas import SignUpModel,LoginUser
from  .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from  .database import Session,engine
from .import JWTtokken
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind = engine)

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):  
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
    )

    session.add(new_user)
    session.commit()  
    session.refresh(new_user)  

    return new_user


@auth_router.get('/get')
async def show_all():
    
    showall = session.query(User).all()
    return jsonable_encoder(showall)



@auth_router.get('/get/{id}')
async def show_all(id:int):
    showone = session.query(User).filter(User.id == id).first()
    if not showone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The given id of {id} id not found')
    return jsonable_encoder(showone)