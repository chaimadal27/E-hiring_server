import datetime

from rest_framework import serializers

from ..models.business_unit_model import BusinessUnit
from ...user_managment.models.profile import Profile


class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = [
            'id',
            'business_unit_name',
            'business_unit_manager',
            'legal_agency',
        ]
        read_only_fields = ['id','legal_agency']

    def create(self, validated_data):
        
        return super().create(validated_data)


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_value(self, dictionary):
        pass



