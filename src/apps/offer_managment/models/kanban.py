# django lib
from django.db import models
from django.conf import settings
# custom lib
from apps.core.behaviors import Authorable, Timestampable
from apps.candidate_managment.models import Candidate
from ..models import Offer
from django.contrib.postgres.fields import ArrayField
from apps.core.models import User


class Kanban(Authorable, Timestampable):
    status_kanban = models.IntegerField(null=True, blank=True)
    stage_candidate = models.IntegerField(choices=settings.STAGE_CANDIDATE, default=settings.TO_SORT_STAGE, null=True,blank=True)
    notes = models.TextField(null=True, blank=True)
    # Foreign Keys
    recruiters = ArrayField(models.IntegerField(),blank=False,null=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE,null=True,)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('candidate', 'offer')
