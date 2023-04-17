from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True)    
    password = models.CharField(max_length=128, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
