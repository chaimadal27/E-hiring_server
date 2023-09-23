from django.db import models
from django.conf import settings

from apps.core.behaviors import Authorable, Timestampable



class LegalAgency(Authorable, Timestampable):
    

    # agency_logo = models.ImageField(upload_to = "LegalAgency/Photo", blank=True)
    agency_name = models.CharField(max_length = 50)
    agency_email = models.EmailField(max_length = 50, unique=True)
    agency_address = models.CharField(max_length = 50)
    agency_postal_code = models.IntegerField()
    agency_city = models.CharField(max_length = 50)
    agency_country = models.CharField(max_length = 50)
    agency_legal_status = models.CharField(max_length = 50)
    load_factor = models.DecimalField(decimal_places=2, max_digits=3)
    load_rate = models.DecimalField(decimal_places=2, max_digits=3)
    number_of_days_open = models.IntegerField(null=True)
    


    @property
    def get_business_units(self):
        businessunit = self.business_unit_set.all().first()


    @staticmethod
    def get_legalAgencies(ids):
        if ids:
            queryset = LegalAgency.objects.filter(id__in = ids)
        else:
            queryset = LegalAgency.objects.all()
            fields = settings.LEGAL_AGENCY_FIELD_CONFIG_CSV
            titles = settings.LEGAL_AGENCY_TITLE_CONFIG_CSV
            return queryset, fields, titles

    class Meta:
        permissions = [
            ('activate_legalagency', 'Can activate legal agency')
        ]
    

    def __str__(self):
        return self.agency_name

    
