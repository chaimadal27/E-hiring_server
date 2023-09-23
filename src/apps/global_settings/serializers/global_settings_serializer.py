from rest_framework import serializers
from ..models.global_settings_model import GlobalSettings
from ...legal_agency.models.legal_agency_model import LegalAgency

class GlobalSettingsSerializer(serializers.ModelSerializer):
    legal_agency = serializers.PrimaryKeyRelatedField(
        read_only = False,
        queryset = LegalAgency.objects.all()
    )
    class Meta:
        model = GlobalSettings
        fields = (
            'id',
            'setting_name',
            'legal_agency',
            'is_global'
        )