import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import datetime, timedelta
from hashids import Hashids

hashids = Hashids(settings.SECRET_KEY, 32)


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        error_messages={'unique': _("A user with that email already exists.")},
    )
    username = models.CharField(
        max_length=150,
        blank=True,)

    first_name_ar = models.CharField(max_length=150, blank=True)
    last_name_ar = models.CharField(max_length=150, blank=True)

    confirm_token = models.TextField(max_length=500, null=True)
    confirm_token_expired_at = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.get_full_name()

    def generate_token(self, db_config_id):
        confirm_token_expired_at = datetime.now() + timedelta(hours=1)
        self.confirm_token_expired_at = confirm_token_expired_at
        self.confirm_token = hashids.encode(db_config_id, self.id)

    def is_confirm_token_expired(self):
        return self.confirm_token_expired_at and self.confirm_token_expired_at > timezone.now()

    @staticmethod
    def decode_generated_token(token):
        return hashids.decode(token)

    def set_groups(self, groups=()):
        user_groups = []
        for grp_name in groups:
            grp = Group.objects.filter(id=grp_name).first()
            grp and user_groups.append(grp)
        if user_groups:
            self.groups.set(user_groups)
