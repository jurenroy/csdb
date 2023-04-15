from django.urls import path
from .views import UserProfileAPIView, ChatAPIView

urlpatterns = [
    path('api/userprofile/', UserProfileAPIView.as_view()),
    path('api/chat/', ChatAPIView.as_view()),
    # add other URLs here as needed
]
