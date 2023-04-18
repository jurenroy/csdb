from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender = models.CharField(max_length=6, blank=True)
    birthday = models.DateField(blank=True, null=True)
    
