from django.contrib import admin

# Register your models here.

from .models import UserProfile, Chat

admin.site.register(UserProfile)
admin.site.register(Chat)
