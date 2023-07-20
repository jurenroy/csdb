from django.contrib import admin
from .models import User
from scheduling.models import Course, Room

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Room)