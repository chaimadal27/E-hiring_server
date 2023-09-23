# python lib
import datetime
# django lib
from rest_framework import serializers, fields
# custom lib
from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name_fr',
                  'first_name_ar',
                  'last_name_fr',
                  'last_name_ar',
                  'email',
                  'telephone',
                  'position',
                  'is_principal',
                  'id'
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
