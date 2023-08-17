from django import forms
from .models import Course, Schedule, RoomSlot

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['coursename', 'abbreviation']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'course', 'section_year', 'section_number', 'subject_code', 'subject_name', 'instructor',
            'lecture_roomslotnumber','lecture_day', 'lecture_starttime', 'lecture_endtime', 'lecture_building_number', 'lecture_roomname',
            'lab_roomslotnumber','lab_day', 'lab_starttime', 'lab_endtime', 'lab_building_number', 'lab_roomname',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lecture_building_number'].queryset = RoomSlot.objects.filter(roomslottype='Lecture', availability=True)
        self.fields['lab_building_number'].queryset = RoomSlot.objects.filter(roomslottype='Lab', availability=True)