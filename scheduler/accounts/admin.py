from django.contrib import admin
from .models import User
from scheduling.models import Course, Room, Subject, Section

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Subject)
admin.site.register(Section)