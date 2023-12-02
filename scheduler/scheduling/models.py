from django.db import models, transaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

# Create your models here.
class CollegeList(models.Model):
    college = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.college
    
class CourseList(models.Model):
    coursename = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    college = models.ForeignKey(CollegeList, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.coursename

class College(models.Model):
    college = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    semester = models.CharField(max_length=100, blank=True, default='First Semester')

    def __str__(self):
        return self.college
    
    
class Course(models.Model):
    coursename = models.CharField(max_length=100, null=True, blank=True)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.coursename

    
class SubjectList(models.Model):
    SEMESTER_CHOICES = [
        ('First Semester', 'First Semester'),
        ('Second Semester', 'Second Semester'),
        ('Summer', 'Summer'),
    ]

    subjectcode = models.CharField(max_length=100, null=True, blank=True)
    subjectname = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, blank=True)
    course = models.ForeignKey(CourseList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subjectcode} - {self.subjectname}"
    

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    year = models.CharField(max_length=20, blank=True)
    subjectcode = models.CharField(max_length=20, blank=True)
    subjectname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.subjectcode} - {self.subjectname}"
    
class Instructor(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
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

class Buildinglist(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    
class Roomlist(models.Model):
    building = models.ForeignKey(Buildinglist, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    roomname = models.CharField(max_length=100, blank=True)
    building_number = models.CharField(max_length=20, blank=True)
    roomtype = models.CharField(max_length=100, blank=True)  # New field for roomtype
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.college} : {self.building_number} - {self.roomname} ( {self.roomtype} )"

class TimeSlot(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True)
    timeslottype = models.CharField(max_length=50)
    starttime = models.TimeField()
    endtime = models.TimeField()

    def __str__(self):
        return f"{self.college} - {self.timeslottype} - {self.starttime} to {self.endtime}"

class RoomSlot(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True)
    roomslottype = models.CharField(max_length=50)
    building_number = models.CharField(max_length=20)
    roomname = models.CharField(max_length=100)
    day = models.CharField(max_length=20)
    starttime = models.TimeField()
    endtime = models.TimeField()
    roomslotnumber = models.PositiveIntegerField(blank=True) 
    availability = models.BooleanField(default=True)  # Add the availability field with a default value of True

    def __str__(self):
        return f"{self.roomslotnumber}: {self.roomname} - {self.roomslottype} - {self.day} - {self.starttime} to {self.endtime}"

@receiver(post_save, sender=TimeSlot)
def create_room_slots_for_timeslot(sender, instance, **kwargs):
    print("Creating room slots for timeslot...")
    timeslottype = instance.timeslottype

    # Days of the week to create room slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    for college in [instance.college]:
        roomtypes = [timeslottype]

        for roomtype in roomtypes:
            for time_slot in TimeSlot.objects.filter(college=college, timeslottype=timeslottype):
                for day in days:
                    room_slots_exist = RoomSlot.objects.filter(
                        college=college,
                        roomslottype=roomtype,
                        day=day,
                        starttime=time_slot.starttime,
                        endtime=time_slot.endtime
                    ).exists()

                    if not room_slots_exist:
                        room_slots_with_same_course_and_type = RoomSlot.objects.filter(college=college, roomslottype=roomtype)
                        roomslotnumber = room_slots_with_same_course_and_type.count() + 1

                        rooms_matching = Room.objects.filter(college=college, roomtype=roomtype)
                        for room in rooms_matching:
                            building_number = room.building_number
                            roomname = room.roomname

                            RoomSlot.objects.create(
                                college=college,
                                roomslottype=roomtype,
                                building_number=building_number,
                                roomname=roomname,
                                day=day,
                                starttime=time_slot.starttime,
                                endtime=time_slot.endtime,
                                roomslotnumber=roomslotnumber,
                                availability=True
                            )
                            roomslotnumber += 1


@receiver(post_save, sender=Room)
def create_room_slots_for_room(sender, instance, created, **kwargs):
    print("Creating room slots for room...")
    if created:
        # Get the college and roomtype of the saved Room instance
        college = instance.college
        roomtype = instance.roomtype

        # Get all timeslots associated with the course and roomtype of the new room
        timeslots = TimeSlot.objects.filter(college=college, timeslottype=roomtype)

        # Days of the week to create room slots
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for time_slot in timeslots:
            for day in days:
                # Check if a room slot with the same attributes already exists
                room_slot_exists = RoomSlot.objects.filter(
                    college=college,
                    roomslottype=roomtype,
                    building_number=instance.building_number,
                    roomname=instance.roomname,
                    day=day,
                    starttime=time_slot.starttime,
                    endtime=time_slot.endtime,
                ).exists()

                if not room_slot_exists:
                    # Get the latest roomslotnumber for the given course and roomtype
                    room_slots_with_same_course_and_type = RoomSlot.objects.filter(
                        college=college,
                        roomslottype=roomtype,
                    ).order_by('-roomslotnumber')

                    if room_slots_with_same_course_and_type.exists():
                        roomslotnumber = room_slots_with_same_course_and_type.first().roomslotnumber + 1
                    else:
                        roomslotnumber = 1

                    # Create the room slot
                    RoomSlot.objects.create(
                        college=college,
                        roomslottype=roomtype,
                        building_number=instance.building_number,
                        roomname=instance.roomname,
                        day=day,
                        starttime=time_slot.starttime,
                        endtime=time_slot.endtime,
                        roomslotnumber=roomslotnumber,
                        availability=True,
                    )


@receiver(pre_delete, sender=Room)
def delete_related_room_slots(sender, instance, **kwargs):
    print("deleting room slots for room...")
    # Delete all related RoomSlot instances when a Room is deleted
    RoomSlot.objects.filter(
        college=instance.college,
        roomslottype=instance.roomtype,
        building_number=instance.building_number,
        roomname=instance.roomname,
    ).delete()

    remaining_room_slots = RoomSlot.objects.filter(college=instance.college, roomslottype=instance.roomtype)
    for index, room_slot in enumerate(remaining_room_slots, start=1):
        room_slot.roomslotnumber = index
        room_slot.save()

@receiver(pre_delete, sender=TimeSlot)
def delete_related_room_slots(sender, instance, **kwargs):
    print("deleting room slots for timeslot...")
    # Delete all related RoomSlot instances when a TimeSlot is deleted
    RoomSlot.objects.filter(
        college=instance.college,
        roomslottype=instance.timeslottype,
        starttime=instance.starttime,
        endtime=instance.endtime,
    ).delete()

    remaining_room_slots = RoomSlot.objects.filter(college=instance.college, roomslottype=instance.timeslottype)
    for index, room_slot in enumerate(remaining_room_slots, start=1):
        room_slot.roomslotnumber = index
        room_slot.save()


@receiver(pre_save, sender=Room)
def update_related_room_slots_for_room(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Room.objects.get(pk=instance.pk)
        except Room.DoesNotExist:
            return  # Ignore if the old instance doesn't exist

        # Check for changes in relevant fields
        if (
            old_instance.college != instance.college or
            old_instance.roomtype != instance.roomtype or
            old_instance.building_number != instance.building_number or
            old_instance.roomname != instance.roomname
        ):
            # Find all related RoomSlot instances based on old values
            related_room_slots = RoomSlot.objects.filter(
                college=old_instance.college,
                roomslottype=old_instance.roomtype,
                building_number=old_instance.building_number,
                roomname=old_instance.roomname,
            )

            # Update the matched RoomSlot instances with the new values
            for room_slot in related_room_slots:
                room_slot.college = instance.college
                room_slot.roomslottype = instance.roomtype
                room_slot.building_number = instance.building_number
                room_slot.roomname = instance.roomname
                room_slot.save()

            # Delete non-matched RoomSlot instances
            non_matched_room_slots = RoomSlot.objects.filter(
                college=old_instance.college,
                roomslottype=old_instance.roomtype,
                building_number=old_instance.building_number,
                roomname=old_instance.roomname,
            ).exclude(pk__in=related_room_slots)
            non_matched_room_slots.delete()

# ...

@receiver(pre_save, sender=TimeSlot)
def update_related_room_slots_for_timeslot(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = TimeSlot.objects.get(pk=instance.pk)
        except TimeSlot.DoesNotExist:
            return  # Ignore if the old instance doesn't exist

        # Check for changes in relevant fields
        if (
            old_instance.college != instance.college or
            old_instance.timeslottype != instance.timeslottype or
            old_instance.starttime != instance.starttime or
            old_instance.endtime != instance.endtime
        ):
            # Find all related RoomSlot instances based on old values
            related_room_slots = RoomSlot.objects.filter(
                college=old_instance.college,
                roomslottype=old_instance.timeslottype,
                starttime=old_instance.starttime,
                endtime=old_instance.endtime,
            )

            # Update the matched RoomSlot instances with the new values
            for room_slot in related_room_slots:
                room_slot.college = instance.college
                room_slot.roomslottype = instance.timeslottype
                room_slot.starttime = instance.starttime
                room_slot.endtime = instance.endtime
                room_slot.save()

            # Delete non-matched RoomSlot instances
            non_matched_room_slots = RoomSlot.objects.filter(
                college=old_instance.college,
                roomslottype=old_instance.timeslottype,
                starttime=old_instance.starttime,
                endtime=old_instance.endtime,
            ).exclude(pk__in=related_room_slots)
            non_matched_room_slots.delete()

class Schedule(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    section_year = models.CharField(max_length=20, null=True, blank=True)  # Field to store year for section
    section_number = models.CharField(max_length=20, null=True, blank=True)  # Field to store section number
    subject_code = models.CharField(max_length=20, null=True, blank=True)  # Field to store subject code
    subject_name = models.CharField(max_length=100, null=True, blank=True)  # Field to store subject name
    instructor = models.CharField(max_length=100, null=True, blank=True)
    
    # Lecture Session
    lecture_roomslotnumber = models.CharField(max_length=20, null=True, blank=True)
    lecture_day = models.CharField(max_length=20, null=True, blank=True)
    lecture_starttime = models.CharField(max_length=50, null=True, blank=True)
    lecture_endtime = models.CharField(max_length=50, null=True, blank=True)
    lecture_building_number = models.CharField(max_length=50, null=True, blank=True)
    lecture_roomname = models.CharField(max_length=50, null=True, blank=True)
    
    # Laboratory Session
    lab_roomslotnumber = models.CharField(max_length=20, null=True, blank=True)
    lab_day = models.CharField(max_length=20, null=True, blank=True)
    lab_starttime = models.CharField(max_length=50, null=True, blank=True)
    lab_endtime = models.CharField(max_length=50, null=True, blank=True)
    lab_building_number = models.CharField(max_length=50, null=True, blank=True)
    lab_roomname = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        year_value = 1
        if self.section_year == "Second Year":
            year_value = 2
        elif self.section_year == "Third Year":
            year_value = 3
        elif self.section_year == "Fourth Year":
            year_value = 4
        return f"{self.course}{year_value}R{self.section_number} ({self.subject_code} - {self.subject_name})"
    

@receiver(post_save, sender=Subject)
@receiver(post_save, sender=Section)
def create_schedule(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Subject):
            course = instance.course
            year = instance.year
            subject_code = instance.subjectcode
            subject_name = instance.subjectname
        elif isinstance(instance, Section):
            course = instance.course
            year = instance.year

        # Check if matching sections and subjects exist
        matching_sections = Section.objects.filter(course=course, year=year)
        matching_subjects = Subject.objects.filter(course=course, year=year)

        if matching_sections.exists() and matching_subjects.exists():
            course_college = course.college
            # Create a Schedule instance for each combination of section and subject
            for matching_section in matching_sections:
                for matching_subject in matching_subjects:
                    Schedule.objects.get_or_create(
                        college=course_college,
                        course=course,
                        section_year=matching_section.year,
                        section_number=matching_section.sectionnumber,
                        subject_code=matching_subject.subjectcode,
                        subject_name=matching_subject.subjectname,
                        defaults={
                            "instructor": "",
                            "lecture_day": "",
                            "lecture_starttime": "",
                            "lecture_endtime": "",
                            "lecture_building_number": "",
                            "lecture_roomname": "",
                            "lab_day": "",
                            "lab_starttime": "",
                            "lab_endtime": "",
                            "lab_building_number": "",
                            "lab_roomname": "",
                        }
                    )

@receiver(pre_delete, sender=Subject)
@receiver(pre_delete, sender=Section)
def delete_related_schedule(sender, instance, **kwargs):
    if isinstance(instance, Subject):
        course = instance.course
        year = instance.year
        subject_code = instance.subjectcode
        subject_name = instance.subjectname
        # Delete related Schedule instances with matching Subject details
        Schedule.objects.filter(
            course=course,
            section_year=year,
            subject_code=subject_code,
            subject_name=subject_name
        ).delete()
    elif isinstance(instance, Section):
        course = instance.course
        year = instance.year
        section_number = instance.sectionnumber
        # Delete related Schedule instances with matching Section details
        Schedule.objects.filter(
            course=course,
            section_year=year,
            section_number=section_number
        ).delete()

@receiver(pre_save, sender=Subject)
def update_related_schedule_for_subject(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Subject.objects.get(pk=instance.pk)
        except Subject.DoesNotExist:
            return  # Ignore if the old instance doesn't exist

        # Check for changes in relevant fields
        if (
            old_instance.course != instance.course or
            old_instance.year != instance.year or
            old_instance.subjectcode != instance.subjectcode or
            old_instance.subjectname != instance.subjectname
        ):
            # Update related Schedule instances with matching Subject details
            Schedule.objects.filter(
                course=old_instance.course,
                section_year=old_instance.year,
                subject_code=old_instance.subjectcode,
                subject_name=old_instance.subjectname
            ).update(
                course=instance.course,
                section_year=instance.year,
                subject_code=instance.subjectcode,
                subject_name=instance.subjectname
            )


@receiver(pre_save, sender=Schedule)
def update_room_slot_availability(sender, instance, **kwargs):
    try:
        old_instance = Schedule.objects.get(pk=instance.pk)
    except Schedule.DoesNotExist:
        return  # Ignore if the old instance doesn't exist

    # Check if lecture_roomslotnumber has changed
    if old_instance.lecture_roomslotnumber != instance.lecture_roomslotnumber:
        if old_instance.lecture_roomslotnumber:
            # Set the availability of the old lecture room slot to True
            RoomSlot.objects.filter(
                roomslotnumber=old_instance.lecture_roomslotnumber,
                roomslottype='Lecture',
                college=instance.college
            ).update(availability=True)

        if instance.lecture_roomslotnumber:
            # Set the availability of the new lecture room slot to False
            RoomSlot.objects.filter(
                roomslotnumber=instance.lecture_roomslotnumber,
                roomslottype='Lecture',
                college=instance.college
            ).update(availability=False)

    # Check if lab_roomslotnumber has changed
    if old_instance.lab_roomslotnumber != instance.lab_roomslotnumber:
        if old_instance.lab_roomslotnumber:
            # Set the availability of the old lab room slot to True
            RoomSlot.objects.filter(
                roomslotnumber=old_instance.lab_roomslotnumber,
                roomslottype='Laboratory',
                college=instance.college
            ).update(availability=True)

        if instance.lab_roomslotnumber:
            # Set the availability of the new lab room slot to False
            RoomSlot.objects.filter(
                roomslotnumber=instance.lab_roomslotnumber,
                roomslottype='Laboratory',
                college=instance.college
            ).update(availability=False)

@receiver(pre_delete, sender=Schedule)
def set_roomslot_availability_on_schedule_delete(sender, instance, **kwargs):
    # Check if the Schedule is deleted
    # Set the availability of lecture and lab room slots back to True
    if instance.lecture_roomslotnumber:
        RoomSlot.objects.filter(
            roomslotnumber=instance.lecture_roomslotnumber,
            roomslottype='Lecture',
            college=instance.college
        ).update(availability=True)

    if instance.lab_roomslotnumber:
        RoomSlot.objects.filter(
            roomslotnumber=instance.lab_roomslotnumber,
            roomslottype='Laboratory',
            college=instance.college
        ).update(availability=True)


@receiver(pre_save, sender=RoomSlot)
def update_schedule_on_roomslot_update(sender, instance, **kwargs):
    # Check if it's an update (not a new creation)
    if instance.pk:
        try:
            old_instance = RoomSlot.objects.get(pk=instance.pk)
        except RoomSlot.DoesNotExist:
            return  # Ignore if the old instance doesn't exist

        # Check if relevant fields have changed
        if (
            old_instance.building_number != instance.building_number or
            old_instance.roomname != instance.roomname or
            old_instance.day != instance.day or
            old_instance.starttime != instance.starttime or
            old_instance.endtime != instance.endtime
        ):
            # Find the corresponding Schedule, if it exists
            try:
                if old_instance.roomslottype == 'Lecture':
                    schedule = Schedule.objects.get(
                        lecture_roomslotnumber=old_instance.roomslotnumber,
                        college=instance.college,
                    )
                    
                    # Update the Lecture fields in Schedule
                    schedule.lecture_roomslotnumber = instance.roomslotnumber
                    schedule.lecture_building_number = instance.building_number
                    schedule.lecture_roomname = instance.roomname
                    schedule.lecture_day = instance.day
                    schedule.lecture_starttime = instance.starttime
                    schedule.lecture_endtime = instance.endtime
                elif old_instance.roomslottype == 'Laboratory':
                    schedule = Schedule.objects.get(
                        lab_roomslotnumber=old_instance.roomslotnumber,
                        college=instance.college,
                    )
                    
                    # Update the Laboratory fields in Schedule
                    schedule.lab_roomslotnumber = instance.roomslotnumber
                    schedule.lab_building_number = instance.building_number
                    schedule.lab_roomname = instance.roomname
                    schedule.lab_day = instance.day
                    schedule.lab_starttime = instance.starttime
                    schedule.lab_endtime = instance.endtime
                
                # Save the Schedule
                schedule.save()
            except Schedule.DoesNotExist:
                pass  # No corresponding Schedule found, do nothing