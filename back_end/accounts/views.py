from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from .models import User

class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        serialized_users = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gender": user.gender,
                "birthday": user.birthday,
            }
            for user in users
        ]
        return JsonResponse(serialized_users, safe=False)