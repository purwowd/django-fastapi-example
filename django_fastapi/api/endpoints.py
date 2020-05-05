from typing import List

from fastapi import APIRouter, Response, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from django.contrib.auth.models import User

from api import models, schemas

security = HTTPBasic()
api_router = APIRouter()


@api_router.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, response: Response, credentials: HTTPBasicCredentials = Depends(security)):

    try:
        user = User.objects.get(username=credentials.username)  # get the user object - if it doesn't exist, the exception block throws unauthorized
        if not user.check_password(credentials.password):  # check the password - if it's wrong, throw 401 unauthorized
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return None
    except User.DoesNotExist:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return None

    item = models.Item.objects.create(**item.dict(), owner_id=user.id)
    response.status_code = status.HTTP_201_CREATED

    return item


@api_router.get("/items", response_model=List[schemas.Item])
def read_items():
    items = list(models.Item.objects.all())

    return items
