from django.db import models
from ...legal_agency.models.legal_agency_model import LegalAgency
class GlobalSettings(models.Model):
    setting_name = models.CharField(max_length = 100, unique=True, null=True)
    legal_agency = models.ForeignKey(LegalAgency, on_delete=models.CASCADE, null=True)
    is_global = models.BooleanField(default = True, null=True)


