from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    pass