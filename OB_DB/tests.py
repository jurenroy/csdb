from django.test import TestCase
from my_app.models import UserProfile

class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.create(
            first_name="John",
            last_name="Doe",
            gender="Male",
            birthday="1990-01-01",
            email="johndoe@example.com",
            password="somepassword",
            profile_pic="profile_pics/johndoe.jpg"
        )
        self.assertEqual(user_profile.__str__(), "John Doe")
