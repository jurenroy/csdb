
from rest_framework import serializers
from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CustomUserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    profile_pic = serializers.ImageField(allow_empty_file=True, required=False)
    isAdmin = serializers.BooleanField(default=False)
    college = serializers.CharField(allow_blank=True, allow_null=True, required=False)


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'profile_pic', 'isAdmin', 'college']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        profile_pic = self.validated_data.pop('profile_pic', None)
        is_admin = self.validated_data.get('isAdmin')
        college = self.validated_data.get('college', None)  # Get the college value

        if is_admin is None:
            is_admin = False

        user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=self.validated_data['password'],
            isAdmin=is_admin,
            college=college  # Save the college value to the user object
        )

        if profile_pic:
            user.profile_pic = profile_pic

        user.is_active = False
        user.save()

        return user

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)