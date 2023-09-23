# python lib
import datetime
from rest_framework import serializers,fields
from ..models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Document
        fields = ['name',
                  'type',
                 # 'is_valid',
                  'file',
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


