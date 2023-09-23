# django lib
from django.db import models
from django.conf import settings

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .partenar import Company


class Contact(Authorable, Timestampable):
    first_name_fr = models.CharField(max_length=30, null=True, blank=True)
    first_name_ar = models.CharField(max_length=30, null=True, blank=True)
    last_name_fr = models.CharField(max_length=30, null=True, blank=True)
    last_name_ar = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=12, blank=True, null=True)
    position = models.CharField(max_length=60, null=True, blank=True)
    is_principal = models.BooleanField(default=False)

    # Foreign Keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name_fr} {self.last_name_fr}"

