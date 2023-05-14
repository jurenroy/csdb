from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import User

User = get_user_model()

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
                "profile_pic": user.profile_pic.url if user.profile_pic else None,
            }
            for user in users
        ]
        return JsonResponse(serialized_users, safe=False)

@csrf_exempt
def update_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        new_profile_pic = request.FILES.get('profile_pic')
        if new_profile_pic:
            user.profile_pic = new_profile_pic
            user.save()
            return HttpResponseRedirect('/profile-updated/')  # Redirect to a success page or the updated profile page

    return render(request, 'update_profile.html', {'user': user})


def profile_updated(request):
    return render(request, 'profile_updated.html')