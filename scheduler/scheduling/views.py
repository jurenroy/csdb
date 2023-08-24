from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Room, Subject, Section, TimeSlot, RoomSlot, Schedule
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .forms import ScheduleForm
import random

# Course views

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        abbreviation = request.POST.get('abbreviation')
        college = request.POST.get('college')  # Add the college field to the form or fetch it from the user session
        if coursename and abbreviation and college:
            course = Course(coursename=coursename, abbreviation=abbreviation, college=college)
            course.save()
            return JsonResponse({'message': 'Course added successfully'})
        else:
            return render(request, 'add_course.html', {'message': 'Invalid course data'})
    else:
        return render(request, 'add_course.html')
    
@csrf_exempt
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return JsonResponse({'message': 'Course deleted successfully'})

@csrf_exempt
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        new_abbreviation = request.POST.get('new_abbreviation')
        college = request.POST.get('college')  # Add the college field to the form or fetch it from the user session

        if coursename and new_abbreviation and college:
            try:
                # Start a transaction to ensure atomicity
                with transaction.atomic():
                    # Check if the new abbreviation is unique
                    if new_abbreviation != course.abbreviation and Course.objects.filter(abbreviation=new_abbreviation).exclude(id=course.id).exists():
                        return JsonResponse({'message': 'Abbreviation already exists'}, status=400)

                    # Update the course fields
                    course.coursename = coursename
                    course.abbreviation = new_abbreviation
                    course.college = college
                    course.save()

                    # Update the affected models (e.g., Section, Room, etc.)
                    Section.objects.filter(course__id=course_id).update(course=course)
                    # Update other affected models as needed

                return JsonResponse({'message': 'Course and affected models updated successfully'})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': 'Invalid course data'}, status=400)
    else:
        return render(request, 'update_course.html', {'course': course})

@csrf_exempt
def get_course_json(request):
    courses = Course.objects.all()
    course_data = [{'courseID': course.id, 'coursename': course.coursename, 'abbreviation': course.abbreviation, 'college': course.college} for course in courses]
    return JsonResponse(course_data, safe=False)


# Room Views

@csrf_exempt
def add_room(request, course_id):
    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        roomtype = request.POST.get('roomtype')  # New field for room type
        if roomname and building_number and roomtype:
            course = get_object_or_404(Course, id=course_id)
            room = Room(roomname=roomname, building_number=building_number, roomtype=roomtype, course=course)
            room.save()
            return JsonResponse({'message': 'Room added successfully'})
        else:
            return render(request, 'add_room.html', {'message': 'Invalid room data'})
    else:
        return render(request, 'add_room.html')

@csrf_exempt
def delete_room(request, course_id, room_id):
    room = get_object_or_404(Room, course__id=course_id, id=room_id)
    room.delete()
    return JsonResponse({'message': 'Room deleted successfully'})

@csrf_exempt
def update_room(request, course_id, room_id):
    room = get_object_or_404(Room, course__id=course_id, id=room_id)

    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        roomtype = request.POST.get('roomtype')

        if roomname and building_number and roomtype:
            room.roomname = roomname
            room.building_number = building_number
            room.roomtype = roomtype
            room.save()
            
            updated_room_data = {
                'roomID': room.id,
                'roomname': room.roomname,
                'building_number': room.building_number,
                'roomtype': room.roomtype,
                'course': room.course.abbreviation if room.course else None
            }
            
            return JsonResponse({'message': 'Room updated successfully', 'room': updated_room_data})
        else:
            return render(request, 'update_room.html', {'room': room, 'message': 'Invalid room data'})
    else:
        return render(request, 'update_room.html', {'room': room})

@csrf_exempt
def get_room_json(request):
    rooms = Room.objects.all()
    room_data = [{'roomID': room.id, 'roomname': room.roomname, 'building_number': room.building_number, 'roomtype': room.roomtype, 'course': room.course.id if room.course else None} for room in rooms]
    return JsonResponse(room_data, safe=False)


#Subject View
@csrf_exempt
def add_subject(request, course_id):
    if request.method == 'POST':
        year = request.POST.get('year')
        subjectcode = request.POST.get('subjectcode')
        subjectname = request.POST.get('subjectname')

        if year and subjectcode and subjectname:
            course = get_object_or_404(Course, id=course_id)
            subject = Subject(course=course, year=year, subjectcode=subjectcode, subjectname=subjectname)
            subject.save()
            return JsonResponse({'message': 'Subject added successfully'})
        else:
            return render(request, 'add_subject.html', {'message': 'Invalid subject data'})
    else:
        return render(request, 'add_subject.html')

@csrf_exempt
def update_subject(request, course_id, subject_id):
    subject = get_object_or_404(Subject, course__id=course_id, id=subject_id)

    if request.method == 'POST':
        year = request.POST.get('year')
        subjectcode = request.POST.get('subjectcode')  # Updated subject code
        subjectname = request.POST.get('subjectname')

        if year and subjectcode and subjectname:
            subject.year = year
            subject.subjectcode = subjectcode  # Update the subject code
            subject.subjectname = subjectname
            subject.save()
            return JsonResponse({'message': 'Subject updated successfully'})
        else:
            return JsonResponse({'message': 'Invalid subject data'})
    else:
        return render(request, 'update_subject.html', {'subject': subject})

@csrf_exempt
def delete_subject(request, course_id, subject_id):
    subject = get_object_or_404(Subject, course__id=course_id, id=subject_id)
    subject.delete()
    return JsonResponse({'message': 'Subject deleted successfully'})

@csrf_exempt
def get_subject_json(request):
    subjects = Subject.objects.all()
    subject_data = [{'subjectID': subject.id, 'subjectcode': subject.subjectcode, 'subjectname': subject.subjectname, 'year': subject.year, 'course': subject.course.id if subject.course else None} for subject in subjects]
    return JsonResponse(subject_data, safe=False)


#Section View
@csrf_exempt
def add_section(request, course_id, year):
    if request.method == 'POST':
        # Count the existing sections for the given course and year
        existing_sections_count = Section.objects.filter(course__id=course_id, year=year).count()

        # Assign the next section number by incrementing the count
        section_number = existing_sections_count + 1

        # Create the new section
        course_obj = get_object_or_404(Course, id=course_id)
        section = Section(course=course_obj, year=year, sectionnumber=section_number)
        section.save()

        return JsonResponse({'message': 'Section added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def delete_section(request, course_id, year):
    if request.method == 'DELETE':
        try:
            # Get the section with the highest section number for the given course and year
            sections = Section.objects.filter(course__id=course_id, year=year)
            if sections.exists():
                highest_section = max(sections, key=lambda section: int(section.sectionnumber))
                section_number = highest_section.sectionnumber
                highest_section.delete()
                return JsonResponse({'message': f'Section {section_number} deleted successfully'})
            else:
                return JsonResponse({'message': 'No sections found for the given course and year'})
        except Exception as e:
            return JsonResponse({'message': 'Error deleting section'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

def get_section_json(request):
    sections = Section.objects.all()
    data = [{'course': section.course.id, 'year': section.year, 'sectionnumber': section.sectionnumber,} for section in sections]
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_selected_rooms(request, abbreviation, roomtype):
    rooms = Room.objects.filter(course__abbreviation=abbreviation, roomtype=roomtype)
    if request.method == 'POST':
        selected_room_ids = request.POST.getlist('room_ids')
        for room_id in selected_room_ids:
            room = get_object_or_404(Room, id=room_id)
            room.delete()
        return JsonResponse({'message': f'Selected {roomtype} rooms deleted successfully'})
    else:
        return render(request, 'delete_selected_rooms.html', {'rooms': rooms, 'roomtype': roomtype})

@csrf_exempt
def delete_all_rooms(request, abbreviation, roomtype):
    rooms = Room.objects.filter(course__abbreviation=abbreviation, roomtype=roomtype)
    if request.method == 'POST':
        rooms.delete()
        return JsonResponse({'message': f'All {roomtype} rooms deleted successfully'})
    else:
        return render(request, 'delete_all_rooms.html', {'rooms': rooms, 'roomtype': roomtype})
    
#Timeslot Views
@csrf_exempt
def add_timeslot(request, course_id):
    if request.method == 'POST':
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        timeslottype = request.POST.get('timeslottype')  # New field for timeslot type
        if starttime and endtime and timeslottype:
            course = get_object_or_404(Course, id=course_id)
            timeslot = TimeSlot(starttime=starttime, endtime=endtime, timeslottype=timeslottype, course=course)
            timeslot.save()
            return JsonResponse({'message': 'Timeslot added successfully'})
        else:
            return render(request, 'add_timeslot.html', {'message': 'Invalid timeslot data'})
    else:
        return render(request, 'add_timeslot.html')

@csrf_exempt
def delete_timeslot(request, course_id, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, course__id=course_id, id=timeslot_id)
    timeslot.delete()
    return JsonResponse({'message': 'Timeslot deleted successfully'})

@csrf_exempt
def update_timeslot(request, course_id, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, course__id=course_id, id=timeslot_id)

    if request.method == 'POST':
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        timeslottype = request.POST.get('timeslottype')  # New field for room type
        if starttime and endtime and timeslottype:
            timeslot.starttime = starttime
            timeslot.endtime = endtime
            timeslot.timeslottype = timeslottype
            timeslot.save()
            return JsonResponse({'message': 'Timeslot updated successfully'})
        else:
            return render(request, 'update_timeslot.html', {'timeslot': timeslot, 'message': 'Invalid timeslot data'})
    else:
        return render(request, 'update_timeslot.html', {'timeslot': timeslot})

@csrf_exempt
def get_timeslot_json(request):
    timeslots = TimeSlot.objects.all()
    timeslot_data = [{'timeslotID': timeslot.id, 'starttime': timeslot.starttime, 'endtime': timeslot.endtime, 'timeslottype': timeslot.timeslottype, 'course': timeslot.course.id if timeslot.course else None} for timeslot in timeslots]
    return JsonResponse(timeslot_data, safe=False)

def get_roomslot_json(request):
    roomslots = RoomSlot.objects.all()
    roomslot_data = [
        {
            'roomslotID': roomslot.id,
            'roomslottype': roomslot.roomslottype,
            'day': roomslot.day,
            'roomname': roomslot.roomname,            
            'building_number': roomslot.building_number,
            'starttime': roomslot.starttime,
            'endtime': roomslot.endtime,
            'roomslotnumber': roomslot.roomslotnumber,
            'availability': roomslot.availability,
            'course': roomslot.course.id if roomslot.course else None
        }
        for roomslot in roomslots
    ]
    return JsonResponse(roomslot_data, safe=False)

def get_schedule_json(request):
    schedules = Schedule.objects.all()
    schedule_data = [
        {
            'scheduleID': schedule.id,
            'course': schedule.course.id if schedule.course else None,
            'section_year': schedule.section_year,
            'section_number': schedule.section_number,
            'subject_code': schedule.subject_code,
            'subject_name': schedule.subject_name,
            'instructor': schedule.instructor,
            'lecture_day': schedule.lecture_day,
            'lecture_starttime': schedule.lecture_starttime,
            'lecture_endtime': schedule.lecture_endtime,
            'lecture_building_number': schedule.lecture_building_number,
            'lecture_roomname': schedule.lecture_roomname,
            'lab_day': schedule.lab_day,
            'lab_starttime': schedule.lab_starttime,
            'lab_endtime': schedule.lab_endtime,
            'lab_building_number': schedule.lab_building_number,
            'lab_roomname': schedule.lab_roomname,
        }
        for schedule in schedules
    ]
    return JsonResponse(schedule_data, safe=False)
    
@csrf_exempt
def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    lecture_roomslots = RoomSlot.objects.filter(course=schedule.course, roomslottype='Lecture', availability=True)
    lab_roomslots = RoomSlot.objects.filter(course=schedule.course, roomslottype='Laboratory', availability=True)
    # Retrieve other necessary roomslots for populating other dropdowns
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Schedule updated successfully'})
        else:
            print("Form is not valid")
            print(form.errors)
            return JsonResponse({'message': 'Invalid schedule data'})
    else:
        form = ScheduleForm(instance=schedule)
    
    context = {
        'form': form,
        'lecture_roomslots': lecture_roomslots,
        'lab_roomslots': lab_roomslots,
        # Add other context variables for other dropdowns
    }
    
    return render(request, 'update_schedule.html', context)

@csrf_exempt
def automate_schedule(request, course_id):
    try:
        # Get the course
        course = Course.objects.get(id=course_id)
        
        # Get available room slots for lectures and laboratories
        available_lecture_slots = RoomSlot.objects.filter(
            course=course,
            roomslottype='Lecture',
            availability=True
        )

        available_lab_slots = RoomSlot.objects.filter(
            course=course,
            roomslottype='Laboratory',
            availability=True
        )

        # Set initial values for filter conditions
        lecture_day = ''
        lecture_starttime = ''
        lecture_endtime = ''
        lab_day = ''
        lab_starttime = ''
        lab_endtime = ''

        # Filter schedules based on initial values
        schedules = Schedule.objects.filter(
            course=course,
            lecture_day=lecture_day,
            lecture_starttime=lecture_starttime,
            lecture_endtime=lecture_endtime,
            lab_day=lab_day,
            lab_starttime=lab_starttime,
            lab_endtime=lab_endtime
        )

        for schedule in schedules:
            if available_lecture_slots.exists():
                random_lecture_slot = random.choice(available_lecture_slots)
                schedule.lecture_day = random_lecture_slot.day
                schedule.lecture_starttime = random_lecture_slot.starttime
                schedule.lecture_endtime = random_lecture_slot.endtime
                schedule.lecture_building_number = random_lecture_slot.building_number
                schedule.lecture_roomname = random_lecture_slot.roomname
                schedule.lecture_roomslotnumber = random_lecture_slot.roomslotnumber  # Assign lecture roomslotnumber
                random_lecture_slot.availability = False
                random_lecture_slot.save()
                available_lecture_slots = available_lecture_slots.exclude(roomslotnumber=random_lecture_slot.roomslotnumber)

            if available_lab_slots.exists():
                random_lab_slot = random.choice(available_lab_slots)
                schedule.lab_day = random_lab_slot.day
                schedule.lab_starttime = random_lab_slot.starttime
                schedule.lab_endtime = random_lab_slot.endtime
                schedule.lab_building_number = random_lab_slot.building_number
                schedule.lab_roomname = random_lab_slot.roomname
                schedule.lab_roomslotnumber = random_lab_slot.roomslotnumber  # Assign lab roomslotnumber
                random_lab_slot.availability = False
                random_lab_slot.save()
                available_lab_slots = available_lab_slots.exclude(roomslotnumber=random_lab_slot.roomslotnumber)

            schedule.save()
            
        if schedules.exists():
            return JsonResponse({'message': 'Scheduling automation completed.'})
        else:
            return JsonResponse({'message': 'No available room slots for scheduling.'})
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'})
