from django.db import models, transaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

# Create your models here.
class Course(models.Model):
    coursename = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.coursename

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['abbreviation'], name='unique_course_abbreviation'),
        ]

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

class Room(models.Model):
    roomname = models.CharField(max_length=100, blank=True)
    building_number = models.CharField(max_length=20, blank=True)
    roomtype = models.CharField(max_length=100, blank=True)  # New field for roomtype
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, to_field='abbreviation')

    def __str__(self):
        return f"{self.course.abbreviation} : {self.building_number} - {self.roomname} ( {self.roomtype} )"

class TimeSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, to_field='abbreviation')
    timeslottype = models.CharField(max_length=50)
    starttime = models.TimeField()
    endtime = models.TimeField()

    def __str__(self):
        return f"{self.course.abbreviation} - {self.timeslottype} - {self.starttime} to {self.endtime}"

class RoomSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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

    for course in [instance.course]:
        roomtypes = [timeslottype]

        for roomtype in roomtypes:
            for time_slot in TimeSlot.objects.filter(course=course, timeslottype=timeslottype):
                for day in days:
                    room_slots_exist = RoomSlot.objects.filter(
                        course=course,
                        roomslottype=roomtype,
                        day=day,
                        starttime=time_slot.starttime,
                        endtime=time_slot.endtime
                    ).exists()

                    if not room_slots_exist:
                        room_slots_with_same_course_and_type = RoomSlot.objects.filter(course=course, roomslottype=roomtype)
                        roomslotnumber = room_slots_with_same_course_and_type.count() + 1

                        rooms_matching = Room.objects.filter(course=course, roomtype=roomtype)
                        for room in rooms_matching:
                            building_number = room.building_number
                            roomname = room.roomname

                            RoomSlot.objects.create(
                                course=course,
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
        # Get the course and roomtype of the saved Room instance
        course = instance.course
        roomtype = instance.roomtype

        # Get all timeslots associated with the course and roomtype of the new room
        timeslots = TimeSlot.objects.filter(course=course, timeslottype=roomtype)

        # Days of the week to create room slots
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for time_slot in timeslots:
            for day in days:
                # Check if a room slot with the same attributes already exists
                room_slot_exists = RoomSlot.objects.filter(
                    course=course,
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
                        course=course,
                        roomslottype=roomtype,
                    ).order_by('-roomslotnumber')

                    if room_slots_with_same_course_and_type.exists():
                        roomslotnumber = room_slots_with_same_course_and_type.first().roomslotnumber + 1
                    else:
                        roomslotnumber = 1

                    # Create the room slot
                    RoomSlot.objects.create(
                        course=course,
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
        course=instance.course,
        roomslottype=instance.roomtype,
        building_number=instance.building_number,
        roomname=instance.roomname,
    ).delete()

    remaining_room_slots = RoomSlot.objects.filter(course=instance.course, roomslottype=instance.roomtype)
    for index, room_slot in enumerate(remaining_room_slots, start=1):
        room_slot.roomslotnumber = index
        room_slot.save()

@receiver(pre_delete, sender=TimeSlot)
def delete_related_room_slots(sender, instance, **kwargs):
    print("deleting room slots for timeslot...")
    # Delete all related RoomSlot instances when a TimeSlot is deleted
    RoomSlot.objects.filter(
        course=instance.course,
        roomslottype=instance.timeslottype,
        starttime=instance.starttime,
        endtime=instance.endtime,
    ).delete()

    remaining_room_slots = RoomSlot.objects.filter(course=instance.course, roomslottype=instance.timeslottype)
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
            old_instance.course != instance.course or
            old_instance.roomtype != instance.roomtype or
            old_instance.building_number != instance.building_number or
            old_instance.roomname != instance.roomname
        ):
            # Find all related RoomSlot instances based on old values
            related_room_slots = RoomSlot.objects.filter(
                course=old_instance.course,
                roomslottype=old_instance.roomtype,
                building_number=old_instance.building_number,
                roomname=old_instance.roomname,
            )

            # Update the matched RoomSlot instances with the new values
            for room_slot in related_room_slots:
                room_slot.course = instance.course
                room_slot.roomslottype = instance.roomtype
                room_slot.building_number = instance.building_number
                room_slot.roomname = instance.roomname
                room_slot.save()

            # Delete non-matched RoomSlot instances
            non_matched_room_slots = RoomSlot.objects.filter(
                course=old_instance.course,
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
            old_instance.course != instance.course or
            old_instance.timeslottype != instance.timeslottype or
            old_instance.starttime != instance.starttime or
            old_instance.endtime != instance.endtime
        ):
            # Find all related RoomSlot instances based on old values
            related_room_slots = RoomSlot.objects.filter(
                course=old_instance.course,
                roomslottype=old_instance.timeslottype,
                starttime=old_instance.starttime,
                endtime=old_instance.endtime,
            )

            # Update the matched RoomSlot instances with the new values
            for room_slot in related_room_slots:
                room_slot.course = instance.course
                room_slot.roomslottype = instance.timeslottype
                room_slot.starttime = instance.starttime
                room_slot.endtime = instance.endtime
                room_slot.save()

            # Delete non-matched RoomSlot instances
            non_matched_room_slots = RoomSlot.objects.filter(
                course=old_instance.course,
                roomslottype=old_instance.timeslottype,
                starttime=old_instance.starttime,
                endtime=old_instance.endtime,
            ).exclude(pk__in=related_room_slots)
            non_matched_room_slots.delete()