import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Appointment
from apps.user_managment.serializers import SimpleUserSerializer
from apps.offer_managment.serializers import OfferSerializer

from ...candidate_managment.models import Candidate
from ...candidate_managment.serializers import CandidateSerializer
from ...referentiel_managment.models import Company
from ...referentiel_managment.serializers import CompanySerialiser

User = get_user_model()


class AppointmentSerializer(serializers.ModelSerializer):
    offer_details = serializers.SerializerMethodField()
    # internParticipants = SimpleUserSerializer(many=True)
    # contactCandidate = CandidateSerializer(many=True)
    # contactEntreprise = CompanySerialiser(many=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'subject',
            'date',
            'start_hour',
            'end_hour',
            'is_done',
            'type',
            'observation_fr',
            'observation_ar',
            'offer',
            'offer_details',
            'participants',
            'entreprises',
            'candidates'
        )
        read_only_fields = (
            'id',
        )

    def get_offer_details(self, obj):
        return OfferSerializer(obj.offer).data

    # TODO: Add check available Appointment
    def create(self, validated_data):
        print(validated_data)
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        return super().update(instance, validated_data)
