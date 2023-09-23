# django lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField



# custom lib
from apps.core.behaviors import Authorable, Timestampable

class List(Authorable, Timestampable):
    """List model contains the unique names and an arrray of values of the lists"""
    name = models.CharField(max_length=200, unique=True)
    #values = ArrayField(models.CharField(max_length=200,blank=True),blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.capitalize()

