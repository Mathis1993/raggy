from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = "users_users"

    username = models.CharField(null=True, blank=True, default=None)  # We don't want to use this field
    email = models.EmailField(_("email address"), unique=True) # Make email field unique

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
