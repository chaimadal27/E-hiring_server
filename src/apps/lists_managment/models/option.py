# django lib
from django.db import models
from django.conf import settings

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .list import List


class Option(Authorable, Timestampable):
    rank = models.IntegerField(default=1)
    value = models.CharField(max_length=200,default='Ajouter une option ici...')

    # Foreign Keys
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.rank} {self.value}"

