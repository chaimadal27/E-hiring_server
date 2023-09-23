from apps.core.mixins.serializers import NestedUpdateMixin, NestedCreateMixin


import datetime
from rest_framework import serializers
from ..models.legal_agency_model import LegalAgency
from ..models.business_unit_model import BusinessUnit
from .business_unit_serializer import BusinessUnitSerializer


    





class LegalAgencySerializer(NestedCreateMixin, NestedUpdateMixin):
    business_unit_set = BusinessUnitSerializer(many = True)
    class Meta:
        model = LegalAgency
        fields = [
            'id',
            'agency_name',
            'agency_email',
            'agency_address',
            'agency_postal_code',
            'agency_city',
            'agency_country',
            'agency_legal_status',
            'load_factor',
            'load_rate',
            'number_of_days_open',
            'business_unit_set',
        ]
        read_only_fields = ['id']
        nested_fields = {'business_unit_set': 'legal_agency'}

