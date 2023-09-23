from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from ..models import Offer
from apps.referentiel_managment.models import Contact
from apps.candidate_managment.models import Candidate
from apps.core.behaviors import Authorable, Timestampable
from django.contrib.auth import get_user_model

from ...referentiel_managment.models import Company

User = get_user_model()

class Appointment(Timestampable, Authorable):
    """Appointment"""
    subject = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=True)
    start_hour = models.TimeField(null=False, blank=False)
    end_hour = models.TimeField(null=False, blank=False)
    is_done = models.BooleanField(default=False)
    type = models.IntegerField(blank=True, null=True)
    observation_fr = models.TextField(null=True, blank=True)
    observation_ar = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    offer = models.ForeignKey(Offer,null=True,blank=True, on_delete=models.CASCADE)
    entreprises = models.ManyToManyField(Company, blank=True, null=True,related_name='entreprises')
    candidates = models.ManyToManyField(Candidate, blank=True, null=True,related_name='candidates')
    participants = models.ManyToManyField(User, blank=True, null=True,related_name='participants')

    class Meta:
        permissions = [
        ]

    def __str__(self):
        return f"{self.subject} {self.date} {self.start_hour} {self.end_hour}"



