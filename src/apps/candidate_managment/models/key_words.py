# django lib
from django.db import models

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .candidate import Candidate


class KeyWords(Authorable, Timestampable):
    value = models.CharField(max_length=100,null=True, blank=True,unique=True)