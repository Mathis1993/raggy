import http

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views import View


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