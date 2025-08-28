import os
import shutil

from core.models import TrackUpdates
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


def delete_user_directory(instance):
    directory = os.path.join(settings.MEDIA_ROOT, f'documents/user_{instance.id}')
    if os.path.isdir(directory):
        shutil.rmtree(directory)


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        db_table = "users_users"

    username = None  # We don't want to use this field
    email = models.EmailField(_("email address"), unique=True)  # Make email field unique
    email_verified = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            UserSettings.objects.get_or_create(user=self)

    def delete(self, using=None, keep_parents=False):
        delete_user_directory(self)
        super().delete(using, keep_parents)


class UserSettings(TrackUpdates):
    class Meta:
        db_table = "users_user_settings"

    class Languages(TextChoices):
        ENGLISH = "english", _("English")
        GERMAN = "german", _("German")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    language = models.CharField(max_length=50, choices=Languages.choices, default=Languages.ENGLISH)
