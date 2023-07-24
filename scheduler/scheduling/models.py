from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, to_field='abbreviation')
    year = models.CharField(max_length=20, blank=True)
    subjectcode = models.CharField(max_length=20, blank=True)
    subjectname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.subjectcode} - {self.subjectname}"
    
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, to_field='abbreviation')
    year = models.CharField(max_length=20)
    sectionnumber = models.CharField(max_length=20)

    def __str__(self):
        year_value = 1
        if self.year == "Second Year":
            year_value = 2
        elif self.year == "Third Year":
            year_value = 3
        elif self.year == "Fourth Year":
            year_value = 4
        return f"{self.course.abbreviation}{year_value}R{self.sectionnumber}"
    
@receiver(post_save, sender=Course)
def create_first_section_for_course(sender, instance, created, **kwargs):
    if created:
        year_levels = ["First Year", "Second Year", "Third Year", "Fourth Year"]
        for year in year_levels:
            section = Section(course=instance, year=year, sectionnumber=1)
            section.save()