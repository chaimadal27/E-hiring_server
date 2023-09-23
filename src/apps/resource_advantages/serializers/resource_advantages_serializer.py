from rest_framework import serializers
from ..models.resource_advantages import ResourceAdvantages


class ResourceAdvantagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceAdvantages
        fields = '__all__'