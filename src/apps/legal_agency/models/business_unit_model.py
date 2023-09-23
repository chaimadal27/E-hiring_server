from django.db import models
from apps.core.behaviors import Authorable, Timestampable
# from ...user_managment.models import Profile
from .legal_agency_model import LegalAgency
# from django.apps.registry import apps
 
# business_unit_manager_FK = apps.get_model('user_management.Profile')

class BusinessUnit(Authorable, Timestampable):

    business_unit_name = models.CharField(max_length = 100)
    legal_agency = models.ForeignKey(LegalAgency, on_delete=models.CASCADE, null=True, related_name="business_unit_set")
    business_unit_manager = models.ManyToManyField('user_managment.Profile')

    

    def __str__(self):
        return self.business_unit_name

    

    class Meta:
        permissions = [
            ('assign_manager','Can assign manager')
        ]
