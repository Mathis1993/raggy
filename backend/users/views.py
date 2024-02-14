import http
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View
from rest_framework import generics

from users.serializers import UserSerializer, UserGeneralInfoSerializer
from users.utils.emails import EmailVerifier, EmailSendingError, PasswordResetter

User = get_user_model()

logger = logging.getLogger(__name__)


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
            if not user.email_verified:
                return JsonResponse(
                    data={"message": "Please verify your email address before logging in."},
                    status=http.HTTPStatus.FORBIDDEN
                )
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse(
                {"message": "This did not work. Please check your email and password."},
                status=http.HTTPStatus.BAD_REQUEST
            )


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "Logout successful"})
        else:
            return JsonResponse(data={"message": "Not logged in"}, status=http.HTTPStatus.BAD_REQUEST)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []  # Signup has to be accessible without authentication
    user = None

    def create(self, request, *args, **kwargs):
        email_verifier = EmailVerifier(host=request.get_host(), scheme=request.scheme, from_email=settings.FROM_EMAIL)
        try:
            response = super().create(request, *args, **kwargs)
            email = response.data.get("email")
            user = User.objects.get(email=email)
            email_verifier.send_verification_email(user)
            return response
        except (ValidationError, User.DoesNotExist) as e:
            return JsonResponse(data={"message": e.message}, status=http.HTTPStatus.BAD_REQUEST)
        except EmailSendingError as e:
            if self.user:
                self.user.delete()
            return JsonResponse(data={"message": e.message}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_user(self) -> User:
        return self.get_serializer().instance


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
            }
        )


class UserInfoUpdateView(generics.UpdateAPIView):
    serializer_class = UserGeneralInfoSerializer

    def get_object(self):
        return self.request.user


class EmailVerificationView(View):
    # ToDo(ME-14.02.24): Improve template
    template_name = "users/verify_email_confirm.html"

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")
        email_verifier = EmailVerifier(host=request.get_host(), scheme=request.scheme, from_email=settings.FROM_EMAIL)
        verified, message = email_verifier.verify_email_for_user(uidb64, token)
        return render(request, self.template_name, context={"verified": verified, "message": message})


class PasswordResetView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            password_resetter = PasswordResetter(host=request.get_host(), scheme=request.scheme, from_email=settings.FROM_EMAIL)
            try:
                password_resetter.send_password_reset_email(user)
            except EmailSendingError:
                logger.warn(f"Could not send password reset email to {email}.")
        return JsonResponse({"message": "If a user with this email exists, a reset link has been sent."})