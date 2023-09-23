# django lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from apps.referentiel_managment.models import Contact,Company
from apps.candidate_managment.models import Candidate
from apps.core.models import User

class Offer(Authorable, Timestampable):
    """offer model fields"""
    title = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(choices=settings.OFFER_STATUS, default=settings.NEW_STATUS,null=True, blank=True)
    positions_number=models.IntegerField(null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    contract_type=models.IntegerField(null=True, blank=True)
    country=models.CharField(max_length=30, blank=True, null=True)
    region=models.CharField(max_length=100, null=True, blank=True)
    client=models.ForeignKey(Company, on_delete=models.RESTRICT,blank=True,null=True)
    contact=models.ForeignKey(Contact, on_delete=models.RESTRICT,blank=True,null=True)
    offer_responsible=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='responsible')
    recruiter = models.ManyToManyField(User, blank=True, null=True,related_name='recruiter')
    seniority = models.IntegerField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    requirements=models.TextField(null=True, blank=True)
    key_words = ArrayField(models.CharField(max_length=50, blank=True), blank=True)
    activity_sector=models.IntegerField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)


    def __str__(self):
        return self.title
