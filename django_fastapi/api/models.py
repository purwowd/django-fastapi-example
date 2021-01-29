from django.db import models
from django.conf import settings


class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()


class User(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
