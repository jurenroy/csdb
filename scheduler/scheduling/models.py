from django.db import models

# Create your models here.
class Course(models.Model):
    coursename = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.coursename

class Room(models.Model):
    roomname = models.CharField(max_length=100, blank=True)
    building_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.roomname
