from django.contrib import admin
from .models import User
from scheduling.models import Course, Room, Subject, Section, TimeSlot, RoomSlot, Schedule

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(TimeSlot)
admin.site.register(RoomSlot)
admin.site.register(Schedule)