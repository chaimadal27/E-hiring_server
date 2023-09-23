# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import Offer
from apps.referentiel_managment.serializers import CompanySerialiser
from apps.core.models import User
from apps.candidate_managment.models import Candidate



class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = [
            'title',
            'status',
            'positions_number',
            'start_date',
            'end_date',
            'contract_type',
            'country',
            'region',
            'client',
            'contact',
            'offer_responsible',
            'recruiter',
            'seniority',
            'description',
            'requirements',
            'key_words',
            'activity_sector',
            'is_active',
            'is_valid',
            'id'
        ]

        read_only_fields = ['id']

    # def create(self, validated_data):
    #     print('************',validated_data)
    #     current_user = self.context.get('request').user
    #     validated_data['created_by'] = current_user
    #     recruiters=validated_data.pop('recruiter')
    #     candidates=validated_data.pop('candidate')
    #     offer = Offer.objects.create(**validated_data)
    #     # for id in recruiters:
    #     #     print(id,"***********************************************")
    #     #     recruiter=User.objects.filter(id=id)
    #     print(recruiters,'++++++++++++++++++++++++++++')
    #     offer.recruiter.set(recruiters)
    #     # for id in recruiters:
    #     #     candidate = Candidate.objects.filter(id=id)
    #     print(candidates,'*****************************')
    #     offer.candidate.set(candidates)
    #     return offer

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        recruiters = validated_data.pop('recruiter')
        print(recruiters, '++++++++++++++++++++++++++++')
        instance.recruiter.set(recruiters)
        print(validated_data)
        return super().update(instance, validated_data)

class OfferListSerializer(serializers.ModelSerializer):
    client_details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = [
            'title',
            'status',
            'client',
            'client_details',
            'is_active',
            'id'
        ]

        read_only_fields = ['id','client_details']

    def get_client_details(self, obj):
        return CompanySerialiser(obj.client).data