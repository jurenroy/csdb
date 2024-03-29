"""
URL configuration for back_end project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import activate_account
from accounts.views import  UserListView, update_profile, profile_updated
from scheduling.views import add_course, delete_course, update_course, get_course_json, add_room, update_room, delete_room, get_room_json, add_subject, update_subject, delete_subject, get_subject_json, add_section, delete_section,get_section_json, add_timeslot, delete_timeslot, update_timeslot, get_timeslot_json, get_roomslot_json, get_schedule_json, update_schedule, automate_schedule, add_instructor, delete_instructor, update_instructor, get_instructor_json, get_buildinglist_json, get_college_json, get_collegelist_json, get_courselist_json,get_roomlist_json, get_subjectlist_json, update_college_semester
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('activation/<uidb64>/<token>/',
         activate_account, name='activate_account'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('update-profile/<str:username>/', update_profile, name='update_profile'),
    path('profile-updated/', profile_updated, name='profile_updated'),
    path('add_course/', add_course, name='add_course'),
    path('delete_course/<str:course_id>/', delete_course, name='delete_course'),
    path('update_course/<str:course_id>/', update_course, name='update_course'),
    path('get_course_json/', get_course_json, name='get_course_json'),
    path('add_instructor/', add_instructor, name='add_instructor'),
    path('delete_instructor/<str:instructor_id>/', delete_instructor, name='delete_instructor'),
    path('update_instructor/<str:instructor_id>/', update_instructor, name='update_instructor'),
    path('get_instructor_json/', get_instructor_json, name='get_instructor_json'),
    path('add_room/<str:college_id>/', add_room, name='add_room'),
    path('delete_room/<str:college_id>/<str:room_id>/', delete_room, name='delete_room'),
    path('update_room/<str:college_id>/<str:room_id>/', update_room, name='update_room'),
    path('get_room_json/', get_room_json, name='get_room_json'),
    path('add_subject/<str:course_id>/', add_subject, name='add_subject'),
    path('delete_subject/<str:course_id>/<str:subject_id>/', delete_subject, name='delete_subject'),
    path('update_subject/<str:course_id>/<str:subject_id>/', update_subject, name='update_subject'),
    path('get_subject_json/', get_subject_json, name='get_subject_json'),
    path('add_section/<str:course_id>/<str:year>/', add_section, name='add_section'),
    path('delete_section/<str:course_id>/<str:year>/', delete_section, name='delete_section'),
    path('get_section_json/', get_section_json, name='get_section_json'),
    path('add_timeslot/<str:college_id>/', add_timeslot, name='add_timeslot'),
    path('delete_timeslot/<str:college_id>/<str:timeslot_id>/', delete_timeslot, name='delete_timeslot'),
    path('update_timeslot/<str:college_id>/<str:timeslot_id>/', update_timeslot, name='update_timeslot'),
    path('get_timeslot_json/', get_timeslot_json, name='get_timeslot_json'),
    path('get_roomslot_json/', get_roomslot_json, name='get_roomslot_json'),
    path('get_schedule_json/', get_schedule_json, name='get_schedule_json'),
    path('automate_schedule/<int:course_id>/', automate_schedule, name='automate_schedule'),
    path('update_schedule/<int:schedule_id>/', update_schedule, name='update_schedule'),

    path('get_college_json/', get_college_json, name='get_college_json'),
    path('get_collegelist_json/', get_collegelist_json, name='get_collegelist_json'),
    path('get_courselist_json/', get_courselist_json, name='get_courselist_json'),
    path('get_buildinglist_json/', get_buildinglist_json, name='get_buildinglist_json'),
    path('get_roomlist_json/', get_roomlist_json, name='get_roomlist_json'),
    path('get_subjectlist_json/', get_subjectlist_json, name='get_subjectlist_json'),

    path('update_college_semester/<int:college_id>/', update_college_semester, name='update_college_semester'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
