from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Room, Subject, Section
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

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
def delete_course(request, abbreviation):
    course = get_object_or_404(Course, abbreviation=abbreviation)
    course.delete()
    return JsonResponse({'message': 'Course deleted successfully'})

@csrf_exempt
def update_course(request, abbreviation):
    course = get_object_or_404(Course, abbreviation=abbreviation)

    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        new_abbreviation = request.POST.get('new_abbreviation')
        college = request.POST.get('college')  # Add the college field to the form or fetch it from the user session

        if coursename and new_abbreviation and college:
            try:
                # Start a transaction to ensure atomicity
                with transaction.atomic():
                    # Update the course fields
                    course.coursename = coursename
                    course.abbreviation = new_abbreviation
                    course.college = college
                    course.save()

                    # Update the affected models (e.g., Section, Room, etc.)
                    Section.objects.filter(course__abbreviation=abbreviation).update(course=course)
                    # Update other affected models as needed

                return JsonResponse({'message': 'Course and affected models updated successfully'})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': 'Invalid course data'}, status=400)
    else:
        return render(request, 'update_course.html', {'course': course})


@csrf_exempt
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@csrf_exempt
def get_course_json(request):
    courses = Course.objects.all()
    course_data = [{'courseID': course.id, 'coursename': course.coursename, 'abbreviation': course.abbreviation, 'college': course.college} for course in courses]
    return JsonResponse(course_data, safe=False)


# Room Views

@csrf_exempt
def add_room(request, abbreviation):
    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        roomtype = request.POST.get('roomtype')  # New field for room type
        if roomname and building_number and roomtype:
            course = get_object_or_404(Course, abbreviation=abbreviation)
            room = Room(roomname=roomname, building_number=building_number, roomtype=roomtype, course=course)
            room.save()
            return JsonResponse({'message': 'Room added successfully'})
        else:
            return render(request, 'add_room.html', {'message': 'Invalid room data'})
    else:
        return render(request, 'add_room.html')

@csrf_exempt
def delete_room(request, abbreviation, roomname):
    room = get_object_or_404(Room, course__abbreviation=abbreviation, roomname=roomname)
    room.delete()
    return JsonResponse({'message': 'Room deleted successfully'})

@csrf_exempt
def update_room(request, abbreviation, roomname):
    room = get_object_or_404(Room, course__abbreviation=abbreviation, roomname=roomname)

    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        roomtype = request.POST.get('roomtype')  # New field for room type
        if roomname and building_number and roomtype:
            room.roomname = roomname
            room.building_number = building_number
            room.roomtype = roomtype
            room.save()
            return JsonResponse({'message': 'Room updated successfully'})
        else:
            return render(request, 'update_room.html', {'room': room, 'message': 'Invalid room data'})
    else:
        return render(request, 'update_room.html', {'room': room})

@csrf_exempt
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@csrf_exempt
def get_room_json(request):
    rooms = Room.objects.all()
    room_data = [{'roomID': room.id, 'roomname': room.roomname, 'building_number': room.building_number, 'roomtype': room.roomtype, 'course': room.course.abbreviation if room.course else None} for room in rooms]
    return JsonResponse(room_data, safe=False)


#Subject View

@csrf_exempt
def add_subject(request, abbreviation):
    if request.method == 'POST':
        year = request.POST.get('year')
        subjectcode = request.POST.get('subjectcode')
        subjectname = request.POST.get('subjectname')

        if year and subjectcode and subjectname:
            course = get_object_or_404(Course, abbreviation=abbreviation)
            subject = Subject(course=course, year=year, subjectcode=subjectcode, subjectname=subjectname)
            subject.save()
            return JsonResponse({'message': 'Subject added successfully'})
        else:
            return render(request, 'add_subject.html', {'message': 'Invalid subject data'})
    else:
        return render(request, 'add_subject.html')

@csrf_exempt
def update_subject(request, abbreviation, subjectcode):
    subject = get_object_or_404(Subject, course__abbreviation=abbreviation, subjectcode=subjectcode)

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
def delete_subject(request, abbreviation, subjectcode):
    subject = get_object_or_404(Subject, course__abbreviation=abbreviation, subjectcode=subjectcode)
    subject.delete()
    return JsonResponse({'message': 'Subject deleted successfully'})

@csrf_exempt
def get_subject_json(request):
    subjects = Subject.objects.all()
    subject_data = [{'subjectcode': subject.subjectcode, 'subjectname': subject.subjectname, 'year': subject.year, 'course': subject.course.abbreviation if subject.course else None} for subject in subjects]
    return JsonResponse(subject_data, safe=False)

#Section View

@csrf_exempt
def add_section(request, course, year):
    if request.method == 'POST':
        # Get the last section number for the given course and year
        last_section = Section.objects.filter(course__abbreviation=course, year=year).order_by('-sectionnumber').first()
        if last_section:
            section_number = int(last_section.sectionnumber) + 1
        else:
            # If no section exists, create the first section with number 1
            section_number = 1

        # Create the new section
        course_obj = get_object_or_404(Course, abbreviation=course)
        section = Section(course=course_obj, year=year, sectionnumber=section_number)
        section.save()

        return JsonResponse({'message': 'Section added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})
    
@csrf_exempt
def delete_section(request, course, year):
    if request.method == 'DELETE':
        # Get the section with the highest section number for the given course and year
        try:
            section = Section.objects.filter(course__abbreviation=course, year=year).order_by('-sectionnumber').first()
            if section:
                if section.sectionnumber == '1':
                    return JsonResponse({'message': 'There is 1 section. Cannot delete the default section.'})
                else:
                    section.delete()
                    return JsonResponse({'message': 'Section deleted successfully'})
            else:
                return JsonResponse({'message': 'No section found for the given course and year'})
        except Exception as e:
            return JsonResponse({'message': 'Error deleting section'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


def get_section_json(request):
    sections = Section.objects.all()
    data = [
        {
            'course': section.course.abbreviation,
            'year': section.year,
            'sectionnumber': section.sectionnumber,
        }
        for section in sections
    ]
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
    
