# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import School

class SchoolSerialiser(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [
            'short_name_fr',
            'long_name_fr',
            'short_name_ar',
            'long_name_ar',
            'web_site',
            'type',
            'country',
            'is_active',
            'id'
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        print(validated_data)
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        # return super().create(validated_data)
        school = School.objects.create(**validated_data)
        return school

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        print(validated_data)
        return super().update(instance, validated_data)
