from django.db import models


class TrackCreation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TrackUpdates(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TrackCreationAndUpdates(TrackCreation, TrackUpdates):
    """
    When creating a django model inheriting from this class,
    no postgres defaults for created_at and update_at fields
    will be set in the database as django manages the default
    values itself.
    If the model should be maintainable via Hasura, the data-
    base default must be set in the migration like this:
    >>>migrations.RunSQL(
    >>>     sql="ALTER TABLE table_name ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP; "
    >>>         "ALTER TABLE table_name ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;",
    >>>     reverse_sql="ALTER TABLE table_name ALTER COLUMN created_at DROP DEFAULT; "
    >>>                 "ALTER TABLE table_name ALTER COLUMN updated_at DROP DEFAULT;"
    >>>    ),
    For automatically updating the updated_at timestamp when updating
    a model field, a postgres trigger must be set on the model table.
    """

    class Meta:
        abstract = True
