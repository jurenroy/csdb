from django.shortcuts import render

# Create your views here.
from .models import Course

def add_course(request):
    if request.method == 'POST':
        name = request.POST['name']
        course = Course(name=name)
        course.save()
        # Optionally, you can redirect to a different page or show a success message.
        return render(request, 'course_added.html')
    else:
        return render(request, 'add_course.html')
