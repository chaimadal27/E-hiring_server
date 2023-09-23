# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import Company, Contact
from .contact_serializer import ContactSerializer


class CompanySerialiser(serializers.ModelSerializer):
    contact_set = ContactSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            'name_fr',
            'name_ar',
            'telephone',
            'email',
            'web_site',
            'activity',
            'address_ar',
            'address_fr',
            'staff',
            'logo',
            'is_active',
            'is_deleted',
            'contact_set',
            'id'
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        contacts_data = validated_data.pop('contact_set')
        validated_data['created_by'] = current_user
        company = Company.objects.create(**validated_data)
        for contact in contacts_data:
            Contact.objects.create(company=company, **contact)
        return company

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        contacts_data = validated_data.pop('contact_set')
        contacts = instance.contact_set.all()
        contacts = list(contacts)
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        instance = super().update(instance, validated_data)
        for contact_data in contacts_data:
            if contacts:
                contact = contacts.pop(0)
                contact.first_name_fr = contact_data.get('first_name_fr')
                contact.first_name_ar = contact_data.get('first_name_ar')
                contact.last_name_fr = contact_data.get('last_name_fr')
                contact.last_name_ar = contact_data.get('last_name_ar')
                contact.email = contact_data.get('email')
                contact.telephone = contact_data.get('telephone')
                contact.position = contact_data.get('position')
                contact.is_principal = contact_data.get('is_principal')
                contact.save()
            else:
                Contact.objects.create(company=instance, **contact_data)
        for contact in contacts:
            contact.delete()

        return instance
