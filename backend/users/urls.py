from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users import views

app_name = "users"

urlpatterns = [
    path("csrf/", views.CSRFTokenView.as_view(), name="csrf"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("info/", views.UserInfoView.as_view(), name="info"),
    path("update/", views.UserInfoUpdateView.as_view(), name="update"),
    path("verify-email/", views.EmailVerificationView.as_view(), name="verify_email"),
    path("request-password-reset/", views.RequestPasswordResetView.as_view(), name="request_password_reset"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("settings/update/", views.UserSettingsUpdateView.as_view(), name="settings_update"),
]
