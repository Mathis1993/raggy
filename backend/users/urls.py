from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = "users"

urlpatterns = [
    path("csrf/", views.CSRFTokenView.as_view(), name="csrf"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # ToDo(ME-03.02.24): Signup
    # ToDo(ME-03.02.24): Password reset
    ]
