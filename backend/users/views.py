import http

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views import View
from rest_framework import serializers
from rest_framework import generics

User = get_user_model()

class CSRFTokenView(View):
    def get(self, request, *args, **kwargs):
        get_token(request)  # Sets a response cookie
        return JsonResponse({"message": "CSRF cookie set"})


class LoginView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=http.HTTPStatus.BAD_REQUEST)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "Logout successful"})
        else:
            return JsonResponse({"message": "Not logged in"}, status=http.HTTPStatus.BAD_REQUEST)


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def validate(self, data):
        # ToDo(ME-08.02.24): Add password strength validation
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            is_superuser=False,
            is_staff=False,
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []  # Signup has to be accessible without authentication
