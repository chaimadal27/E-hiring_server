# django lib
from django.db import models
# from apps.offer_managment.models import Offer

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .candidate import Candidate


class LanguageDetail(Authorable, Timestampable):
    language = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)

    # Foreign Keys
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    #offer = models.ForeignKey(Offer, on_delete=models.CASCADE,null=True, blank=True)