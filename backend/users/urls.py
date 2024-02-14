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
    path("verify-email/<uidb64>/<token>/", views.EmailVerificationView.as_view(), name="verify_email"),
    path("reset-password/", views.PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            # ToDo(ME-14.02.24): Add own template
            # template_name="",
            # ToDo(ME-14.02.24): Probably also add own form
            # form_class=MyForm,
            success_url=reverse_lazy("users:reset_password_complete"),
        ),
        name="reset_password_confirm",
    ),
    path(
        "reset-password-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            # ToDo(ME-14.02.24): Add own template
            # template_name=""
        ),
        name="reset_password_complete",
    ),
]
