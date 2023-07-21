from django.db import models

# Create your models here.
class Course(models.Model):
    coursename = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.coursename

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['abbreviation'], name='unique_course_abbreviation'),
        ]

class Room(models.Model):
    roomname = models.CharField(max_length=100, blank=True)
    building_number = models.CharField(max_length=20, blank=True)
    roomtype = models.CharField(max_length=100, blank=True)  # New field for roomtype
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, to_field='abbreviation')

    def __str__(self):
        return self.roomname
