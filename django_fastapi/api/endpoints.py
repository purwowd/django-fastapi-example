from typing import List

from fastapi import APIRouter, Response, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from api import models, schemas

security = HTTPBasic()
api_router = APIRouter()


@api_router.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, response: Response, credentials: HTTPBasicCredentials = Depends(security)):

    user = authenticate(username=credentials.username, password=credentials.password)
    if user is not None:
        item = models.Item.objects.create(**item.dict(), owner_id=user.id)
        response.status_code = status.HTTP_201_CREATED
        return item
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return None


@api_router.get("/items", response_model=List[schemas.Item])
def read_items():
    items = list(models.Item.objects.all())

    return items
