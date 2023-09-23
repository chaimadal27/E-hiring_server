from django.db import models

from ...core.behaviors import Timestampable, Authorable
class ActivityType(Timestampable, Authorable):
    activity_type_name = models.CharField(max_length=20)
    business_unit = models.ManyToManyField('legal_agency.BusinessUnit')

    def __str__(self):
        return self.activity_type_name
