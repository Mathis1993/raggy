from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = "users"

urlpatterns = [
    path("csrf/", views.CSRFTokenView.as_view(), name="csrf"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("info/", views.UserInfoView.as_view(), name="info"),
    path("update/", views.UserInfoUpdateView.as_view(), name="update"),
    path("verify-email-confirm/<uidb64>/<token>/", views.EmailVerificationView.as_view(), name="verify_email"),
    # ToDo(ME-03.02.24): Password reset
]
