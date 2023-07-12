from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from django.http import JsonResponse

# Create your views here.

def add_course(request):
    if request.method == 'POST':
        coursename = request.POST['coursename']
        abbreviation = request.POST['abbreviation']
        course = Course(coursename=coursename, abbreviation=abbreviation)
        course.save()
        return redirect('course_list')
    else:
        return render(request, 'add_course.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('course_list')

def update_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        coursename = request.POST['coursename']
        abbreviation = request.POST['abbreviation']
        course.coursename = coursename
        course.abbreviation = abbreviation
        course.save()
        return redirect('course_list')
    else:
        return render(request, 'update_course.html', {'course': course})

def get_course_json(request):
    courses = Course.objects.all()
    course_data = [{'courseID': course.id,'coursename': course.coursename, 'abbreviation': course.abbreviation} for course in courses]
    return JsonResponse(course_data, safe=False)
