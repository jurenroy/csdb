from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Room
from django.views.decorators.csrf import csrf_exempt

# Course views

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        abbreviation = request.POST.get('abbreviation')
        if coursename and abbreviation:
            course = Course(coursename=coursename, abbreviation=abbreviation)
            course.save()
            return JsonResponse({'message': 'Course added successfully'})
        else:
            return render(request, 'add_course.html', {'message': 'Invalid course data'})
    else:
        return render(request, 'add_course.html')
    
@csrf_exempt
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete
    return JsonResponse({'message': 'Course deleted successfully'})

@csrf_exempt
def update_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        abbreviation = request.POST.get('abbreviation')
        if coursename and abbreviation:
            course.coursename = coursename
            course.abbreviation = abbreviation
            course.save()
            return JsonResponse({'message': 'Course updated successfully'})
        else:
            return render(request, 'update_course.html', {'course': course, 'message': 'Invalid course data'})
    else:
        return render(request, 'update_course.html', {'course': course})

@csrf_exempt
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@csrf_exempt
def get_course_json(request):
    courses = Course.objects.all()
    course_data = [{'courseID': course.id, 'coursename': course.coursename, 'abbreviation': course.abbreviation} for course in courses]
    return JsonResponse(course_data, safe=False)


# Room views

@csrf_exempt
def add_room(request):
    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        if roomname and building_number:
            room = Room(roomname=roomname, building_number=building_number)
            room.save()
            return JsonResponse({'message': 'Room added successfully'})
        else:
            return render(request, 'add_room.html', {'message': 'Invalid room data'})
    else:
        return render(request, 'add_room.html')

@csrf_exempt
def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.delete
    return JsonResponse({'message': 'Room deleted successfully'})

@csrf_exempt
def update_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        roomname = request.POST.get('roomname')
        building_number = request.POST.get('building_number')
        if roomname and building_number:
            room.roomname = roomname
            room.building_number = building_number
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
    room_data = [{'roomID': room.id, 'roomname': room.roomname, 'building_number': room.building_number} for room in rooms]
    return JsonResponse(room_data, safe=False)
