from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from core.models import TrackUpdates


class User(AbstractUser):
    class Meta:
        db_table = "users_users"

    username = models.CharField(null=True, blank=True, default=None)  # We don't want to use this field
    email = models.EmailField(_("email address"), unique=True) # Make email field unique

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            UserSettings.objects.get_or_create(user=self)
        super().save(*args, **kwargs)


class UserSettings(TrackUpdates):

    class Meta:
        db_table = "users_user_settings"

    class Languages(TextChoices):
        ENGLISH = "english", _("English")
        GERMAN = "german", _("German")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    language = models.CharField(max_length=50, choices=Languages.choices, default=Languages.ENGLISH)
