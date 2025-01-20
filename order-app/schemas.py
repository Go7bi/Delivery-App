from pydantic import BaseModel, EmailStr
from typing import List,Optional


class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            'example': {
                "username": "gobi",
                "email": "gobi@gmail.com",
                "password": "password",
            }
        }

class LoginUser(BaseModel):
    email: str
    password: str

class OrderModel(BaseModel):
    quantity:int
    pizza_size:Optional[str]="SMALL"
    address : str



    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email:  str


class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        json_schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }