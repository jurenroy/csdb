from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    isAdmin = models.BooleanField(blank=True, null=True)
    college = models.CharField(max_length=100, blank=True)
    