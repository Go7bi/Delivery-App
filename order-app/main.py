from fastapi import FastAPI,Depends,status,Response,HTTPException
from typing import List
from  .database import engine
from  .user_routers import auth_router
from .order_routers import order_router
from .authentication import singn_router
from .import models




app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(singn_router)
app.include_router(auth_router)
app.include_router(order_router)
