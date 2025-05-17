from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 필요시 확장 가능
    pass