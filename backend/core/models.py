from django.db import models

class TrackCreation(models.Model):
    """
    Abstract model that tracks the creation date of a model instance.
    """

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
