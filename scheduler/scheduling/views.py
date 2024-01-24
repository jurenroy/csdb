from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import College, CollegeList, CourseList, Course, Room, Roomlist, Buildinglist, SubjectList, Subject, Section, TimeSlot, RoomSlot, Schedule, Instructor
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .forms import ScheduleForm
from django.db.models import Q
from django.http import HttpResponse
import random

# Course views

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        abbreviation = request.POST.get('abbreviation')
        college_id = request.POST.get('college')  # Get college ID from the request
        if coursename and abbreviation and college_id:
            # Retrieve the College instance based on the provided college ID
            college = get_object_or_404(College, id=college_id)

            # Create and save the Course instance
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

#Instructor Views

@csrf_exempt
def add_instructor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        college_id = request.POST.get('college')  # Assuming you receive the college ID in the form
        if name and college_id:
            college = get_object_or_404(College, id=college_id)
            instructor = Instructor(name=name, college=college)
            instructor.save()
            return JsonResponse({'message': 'Instructor added successfully'})
        else:
            return JsonResponse({'message': 'Invalid instructor data'}, status=400)
    else:
        return render(request, 'add_instructor.html')
    
@csrf_exempt
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    instructor.delete()
    return JsonResponse({'message': 'Instructor deleted successfully'})

@csrf_exempt
def update_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        college_id = request.POST.get('college')  # Assuming you receive the college ID in the form

        if new_name and college_id:
            try:
                with transaction.atomic():
                    if new_name != instructor.name and Instructor.objects.filter(name=new_name).exclude(id=instructor.id).exists():
                        return JsonResponse({'message': 'Instructor already exists'}, status=400)

                    college = get_object_or_404(College, id=college_id)
                    instructor.name = new_name
                    instructor.college = college
                    instructor.save()

                return JsonResponse({'message': 'Instructor updated successfully'})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': 'Invalid instructor data'}, status=400)
    else:
        return render(request, 'update_instructor.html', {'instructor': instructor})

@csrf_exempt
def get_instructor_json(request):
    instructors = Instructor.objects.all()
    instructor_data = [{'instructorID': instructor.id, 'name': instructor.name, 'college': instructor.college.id} for instructor in instructors]
    return JsonResponse(instructor_data, safe=False)

# Room Views

@csrf_exempt
def add_room(request, college_id):
    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        roomtype = request.POST.get('roomtype')  # New field for room type
        if roomname and building_number and roomtype:
            college = get_object_or_404(College, id=college_id)
            room = Room(roomname=roomname, building_number=building_number, roomtype=roomtype, college=college)
            room.save()
            return JsonResponse({'message': 'Room added successfully'})
        else:
            return render(request, 'add_room.html', {'message': 'Invalid room data'})
    else:
        return render(request, 'add_room.html')

@csrf_exempt
def delete_room(request, college_id, room_id):
    room = get_object_or_404(Room, college__id=college_id, id=room_id)
    room.delete()
    return JsonResponse({'message': 'Room deleted successfully'})

@csrf_exempt
def update_room(request, college_id, room_id):
    room = get_object_or_404(Room, college__id=college_id, id=room_id)

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
                'college': room.college.abbreviation if room.college else None
            }
            
            return JsonResponse({'message': 'Room updated successfully', 'room': updated_room_data})
        else:
            return render(request, 'update_room.html', {'room': room, 'message': 'Invalid room data'})
    else:
        return render(request, 'update_room.html', {'room': room})

@csrf_exempt
def get_room_json(request):
    rooms = Room.objects.all()
    room_data = [{'roomID': room.id, 'roomname': room.roomname, 'building_number': room.building_number, 'roomtype': room.roomtype, 'college': room.college.id if room.college else None} for room in rooms]
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
def add_timeslot(request, college_id):
    if request.method == 'POST':
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        timeslottype = request.POST.get('timeslottype')  # New field for timeslot type
        if starttime and endtime and timeslottype:
            college = get_object_or_404(College, id=college_id)
            timeslot = TimeSlot(starttime=starttime, endtime=endtime, timeslottype=timeslottype, college=college)
            timeslot.save()
            return JsonResponse({'message': 'Timeslot added successfully'})
        else:
            return render(request, 'add_timeslot.html', {'message': 'Invalid timeslot data'})
    else:
        return render(request, 'add_timeslot.html')

@csrf_exempt
def delete_timeslot(request, college_id, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, college__id=college_id, id=timeslot_id)
    timeslot.delete()
    return JsonResponse({'message': 'Timeslot deleted successfully'})

@csrf_exempt
def update_timeslot(request, college_id, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, college__id=college_id, id=timeslot_id)

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
    timeslot_data = [{'timeslotID': timeslot.id, 'starttime': timeslot.starttime, 'endtime': timeslot.endtime, 'timeslottype': timeslot.timeslottype, 'college': timeslot.college.id if timeslot.college else None} for timeslot in timeslots]
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
            'college': roomslot.college.id if roomslot.college else None
        }
        for roomslot in roomslots
    ]
    return JsonResponse(roomslot_data, safe=False)

def get_schedule_json(request):
    schedules = Schedule.objects.all()
    schedule_data = [
        {
            'scheduleID': schedule.id,
            'college': schedule.college.id if schedule.college else None,
            'course': schedule.course.id if schedule.course else None,
            'section_year': schedule.section_year,
            'section_number': schedule.section_number,
            'subject_code': schedule.subject_code,
            'subject_name': schedule.subject_name,
            'instructor': schedule.instructor,
            'lecture_roomslotnumber': schedule.lecture_roomslotnumber,
            'lecture_day': schedule.lecture_day,
            'lecture_starttime': schedule.lecture_starttime,
            'lecture_endtime': schedule.lecture_endtime,
            'lecture_building_number': schedule.lecture_building_number,
            'lecture_roomname': schedule.lecture_roomname,
            'lab_roomslotnumber': schedule.lab_roomslotnumber,
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
    
    lecture_roomslots = RoomSlot.objects.filter(college=schedule.college, roomslottype='Lecture', availability=True)
    lab_roomslots = RoomSlot.objects.filter(college=schedule.college, roomslottype='Laboratory', availability=True)
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
        college = course.college
        
        # Get available room slots for lectures and laboratories
        available_lecture_slots = RoomSlot.objects.filter(
            college=college,
            roomslottype='Lecture',
            availability=True
        )

        available_lab_slots = RoomSlot.objects.filter(
            college=college,
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
            college=college,
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


@csrf_exempt
def get_college_json(request):
    colleges = College.objects.all()
    college_data = [{'collegeID': college.id, 'college': college.college, 'abbreviation': college.abbreviation, 'semester': college.semester} for college in colleges]
    return JsonResponse(college_data, safe=False)

@csrf_exempt
def get_collegelist_json(request):
    collegelists = CollegeList.objects.all()
    collegelist_data = [{'collegelistID': collegelist.id,'college': collegelist.college, 'abbreviation': collegelist.abbreviation} for collegelist in collegelists]
    return JsonResponse(collegelist_data, safe=False)

@csrf_exempt
def get_courselist_json(request):
    courselists = CourseList.objects.all()
    courselist_data = [
        {
            'courselistID': courselist.id,
            'coursename': courselist.coursename,
            'abbreviation': courselist.abbreviation,
            'college': courselist.college.id,
        }
        for courselist in courselists
    ]
    return JsonResponse(courselist_data, safe=False)

@csrf_exempt
def get_buildinglist_json(request):
    buildinglists = Buildinglist.objects.all()
    buildinglist_data = [{'buildinglistID': buildinglist.id, 'name': buildinglist.name} for buildinglist in buildinglists]
    return JsonResponse(buildinglist_data, safe=False)

@csrf_exempt
def get_roomlist_json(request):
    roomlists = Roomlist.objects.all()
    roomlist_data = [{'roomlistID': roomlist.id, 'roomname': roomlist.roomname, 'building': roomlist.building} for roomlist in roomlists]
    return JsonResponse(roomlist_data, safe=False)

@csrf_exempt
def get_subjectlist_json(request):
    subjectlists = SubjectList.objects.all()
    subjectlist_data = [{'subjectlistID': subjectlist.id, 'subjectcode': subjectlist.subjectcode, 'subjectname': subjectlist.subjectname,'year': subjectlist.year, 'semester': subjectlist.semester,'course': subjectlist.course} for subjectlist in subjectlists]
    return JsonResponse(subjectlist_data, safe=False)


@csrf_exempt
def update_college_semester(request, college_id):
    college = get_object_or_404(College, id=college_id)

    if request.method == 'POST':
        new_semester = request.POST.get('semester')

        if new_semester:
            # Update the semester for the college
            college.semester = new_semester
            college.save()

            # Delete all courses associated with the college
            courses_to_delete = Course.objects.filter(college=college)
            courses_to_delete.delete()
            
            # Delete all rooms associated with the college
            rooms_to_delete = Room.objects.filter(college=college)
            rooms_to_delete.delete()

            # Delete all timeslots associated with the college
            timeslots_to_delete = TimeSlot.objects.filter(college=college)
            timeslots_to_delete.delete()

            # Delete all instructor associated with the college
            timeslots_to_delete = Instructor.objects.filter(college=college)
            timeslots_to_delete.delete()

            return JsonResponse({'message': 'College semester updated successfully'})
        else:
            return JsonResponse({'message': 'Invalid semester data'})
    else:
        return render(request, 'update_college_semester.html', {'college': college})
    

def update_availability(request):
    # #1 Get all existing RoomSlot instances
    all_slots = RoomSlot.objects.all()

    # Define a custom sorting key function
    def custom_sort_key(slot):
        # Sort by availability (False first)
        return (slot.availability, slot.building_number, slot.roomname, slot.day, slot.starttime, slot.endtime)

    # Sort all_slots using the custom_sort_key
    sorted_slots = sorted(all_slots, key=custom_sort_key)

    # Now, sorted_slots contains the sorted RoomSlot instances

    # #2 Iterate over each RoomSlot instance (i)
    for i in sorted_slots:
        # #2.1 Check if the instance has been used in a schedule
        print(f"RoomSlot: {i.roomslottype} - {i.building_number} - {i.roomname} - {i.day} - {i.roomslotnumber}")
        # Update the query to use Q objects for more complex conditions
        is_used_in_schedule = Schedule.objects.filter(
            Q(college=i.college) &
            (
                (Q(lecture_building_number=i.building_number) & Q(lecture_roomname=i.roomname) & Q(lecture_day=i.day) & Q(lecture_roomslotnumber=i.roomslotnumber)) |
                (Q(lab_building_number=i.building_number) & Q(lab_roomname=i.roomname) & Q(lab_day=i.day) & Q(lab_roomslotnumber=i.roomslotnumber))
            )
        ).exists()
        print(f"is_used_in_schedule: {is_used_in_schedule}")

        # If the instance is used in a schedule, set availability to False and continue to the next iteration
        if is_used_in_schedule:
            i.availability = False
            i.save()
            continue

        # If the instance is not used in a schedule, set availability to True
        i.availability = True

        # #2.1 Exclude the current instance (i) from the comparison
        conflicting_slots = all_slots.filter(
            building_number=i.building_number,
            roomname=i.roomname,
            day=i.day,
        ).exclude(pk=i.pk)

        # #2.2 Check if there are any conflicting instances with time overlap
        conflicting_instances = [
            j for j in conflicting_slots
            if i.starttime < j.endtime and i.endtime > j.starttime
        ]

        # #2.3 Check if there is any conflicting instance with availability=False
        if conflicting_instances:
            has_conflict_false = any(
                not conflict.availability for conflict in conflicting_instances
            )
            # #2.4 Set availability based on conflicts
            i.availability = not has_conflict_false
        else:
            # Preserve the existing availability if there are no conflicts
            i.availability = i.availability

        # Save the instance
        i.save()

        return HttpResponse("Availability updated successfully.")

