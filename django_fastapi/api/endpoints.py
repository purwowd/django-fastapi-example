from typing import List

from fastapi import APIRouter, Response, status, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from project.jwt import JWTBearer, signJWT

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from api import models, schemas


users = []


def check_user(data: schemas.UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


security = HTTPBasic()
api_router = APIRouter()


@api_router.post("/items", dependencies=[Depends(JWTBearer())], response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, response: Response):
    item = models.Item.objects.create(**item.dict())
    response.status_code = status.HTTP_201_CREATED

    return item


@api_router.get("/items", dependencies=[Depends(JWTBearer())], response_model=List[schemas.Item])
def read_items():
    items = list(models.Item.objects.all())

    return items


@api_router.post("/user/signup", tags=["user"])
async def create_user(user: schemas.UserCreate = Body(...)):
    users.append(user)  # replace with db call, making sure to hash the password first
    user = User.objects.create(username=user.name, email=user.email, password=user.password)
    return signJWT(user.email)


@api_router.post("/user/login", tags=["user"])
async def user_login(user: schemas.UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
