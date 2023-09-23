from django.db import models


class UserDBConfig(models.Model):

    unique_config = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    auth_field = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    db_name = models.CharField(max_length=150, blank=False)
