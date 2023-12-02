from django.contrib import admin
from .models import User
from scheduling.models import Course, Room, Subject, Section, TimeSlot, RoomSlot, Schedule, College, CollegeList, CourseList, Roomlist, Buildinglist, SubjectList

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(TimeSlot)
admin.site.register(RoomSlot)
admin.site.register(Schedule)
admin.site.register(College)
admin.site.register(CollegeList)
admin.site.register(CourseList)
admin.site.register(Buildinglist)
admin.site.register(Roomlist)
admin.site.register(SubjectList)