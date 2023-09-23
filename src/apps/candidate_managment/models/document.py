# django lib
from django.db import models

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .candidate import Candidate


class Document(Authorable, Timestampable):
    name = models.CharField(max_length=300,null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    file = models.FileField(upload_to="Candidates/documents", blank=True, null=True)
    #is_valid = models.BooleanField(default=False)
    # Foreign Keys
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)