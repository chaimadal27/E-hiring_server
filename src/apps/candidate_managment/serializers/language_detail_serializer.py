# python lib
import datetime
# django lib
from rest_framework import serializers, fields
# custom lib
from ..models import LanguageDetail


class LanguageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageDetail
        fields = ['language',
                  'level',
                  'id',
                  ]
        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        print(validated_data)
        return super().update(instance, validated_data)
