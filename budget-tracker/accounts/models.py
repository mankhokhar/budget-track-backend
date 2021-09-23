from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

