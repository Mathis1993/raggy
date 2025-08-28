import http
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView

from users.serializers import UserSerializer, UserGeneralInfoSerializer, UserSettingsSerializer
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
            # if not user.email_verified:
            #     return JsonResponse(
            #         data={"message": "Please verify your email address before logging in."},
            #         status=http.HTTPStatus.FORBIDDEN
            #     )
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
        base_url = request.META.get('HTTP_ORIGIN', request.get_host())
        email_verifier = EmailVerifier(base_url=base_url, from_email=settings.FROM_EMAIL)
        try:
            response = super().create(request, *args, **kwargs)
            email = response.data.get("email")
            user = User.objects.get(email=email)
            email_verifier.send_verification_email(user)
            return response
        except (ValidationError, User.DoesNotExist) as e:
            logger.error(e.message)
            return JsonResponse(data={"message": e.message}, status=http.HTTPStatus.BAD_REQUEST)
        except EmailSendingError as e:
            if self.user:
                self.user.delete()
            return JsonResponse(data={"message": e.message}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_user(self) -> User:
        return self.get_serializer().instance


class UserInfoView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserGeneralInfoSerializer(request.user)
        return JsonResponse(serializer.data)


class UserInfoUpdateView(generics.UpdateAPIView):
    serializer_class = UserGeneralInfoSerializer

    def get_object(self):
        return self.request.user


class EmailVerificationView(View):
    def post(self, request, *args, **kwargs):
        uidb64 = request.POST.get("uidb64")
        token = request.POST.get("token")
        base_url = request.META.get('HTTP_ORIGIN', request.get_host())
        email_verifier = EmailVerifier(base_url=base_url, from_email=settings.FROM_EMAIL)
        verified, message = email_verifier.verify_email_for_user(uidb64, token)
        return JsonResponse({"verified": verified, "message": message})


class RequestPasswordResetView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        base_url = request.META.get('HTTP_ORIGIN', request.get_host())
        if user:
            password_resetter = PasswordResetter(base_url=base_url, from_email=settings.FROM_EMAIL)
            try:
                password_resetter.send_password_reset_email(user)
            except EmailSendingError:
                logger.warning(f"Could not send password reset email to {email}.")
        return JsonResponse({"message": "If a user with this email exists, a reset link has been sent."})


class ResetPasswordView(View):
    def post(self, request, *args, **kwargs):
        uidb64 = request.POST.get("uidb64")
        token = request.POST.get("token")
        base_url = request.META.get('HTTP_ORIGIN', request.get_host())
        password_resetter = PasswordResetter(base_url=base_url, from_email=settings.FROM_EMAIL)
        success, message = password_resetter.verify(uidb64, token)
        if not success:
            return JsonResponse({"message": message}, status=http.HTTPStatus.BAD_REQUEST)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        password_data = {"password1": password1, "password2": password2 }
        serializer = UserSerializer(data=password_data)
        try:
            serializer.validate(password_data)
        except ValidationError as e:
            return JsonResponse(data=e.message_dict, status=http.HTTPStatus.BAD_REQUEST)
        user = password_resetter.get_user(uidb64)
        user.set_password(password1)
        user.save()
        return JsonResponse({"message": "Password reset successful"})


class UserSettingsUpdateView(generics.UpdateAPIView):
    serializer_class = UserSettingsSerializer

    def get_object(self):
        return self.request.user.settings

    def put(self, request, *args, **kwargs):
        print(request.data)
        return super().put(request, *args, **kwargs)
