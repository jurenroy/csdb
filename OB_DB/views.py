from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import UserProfile

class UserProfileCreateView(CreateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'gender', 'birthday', 'email', 'password', 'profile_pic']
    success_url = reverse_lazy('home')
    template_name = 'userprofile_form.html'

def home(request):
    return render(request, 'home.html')
