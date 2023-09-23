# python lib
import datetime
from rest_framework import serializers, fields
from django.conf import settings
# custom lib
from ..models import Kanban
from apps.candidate_managment.models import Candidate
# signals imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.candidate_managment.serializers import CandidateKanbanSerializer
from apps.offer_managment.serializers import OfferListSerializer
from apps.user_managment.serializers import SimpleUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class KanbanSerializer(serializers.ModelSerializer):
    candidate_details = serializers.SerializerMethodField()
    recruiter_details = serializers.SerializerMethodField()
    offer_details = serializers.SerializerMethodField()
    class Meta:
        model = Kanban
        fields = ['status_kanban',
                  'stage_candidate',
                  'notes',
                  'recruiters',
                  'candidate',
                  'offer',
                  'created_at',
                  'candidate_details',
                  'recruiter_details',
                  'offer_details',
                  'id']
        read_only_fields = ['id','candidate_details','recruiter_details','offer_details']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        return super().update(instance, validated_data)

    def get_candidate_details(self, obj):
        return CandidateKanbanSerializer(obj.candidate).data

    def get_recruiter_details(self, obj):
        users=[]
        for recruiter in obj.recruiters:
            user=User.objects.get(id=recruiter)
            users.append(SimpleUserSerializer(user).data)
        return users
    def get_offer_details(self, obj):
        return OfferListSerializer(obj.offer).data

@receiver(post_save, sender=Kanban)
def kanban_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    if created:
        candidate_id=instance.candidate.id
        candidate=Candidate.objects.get(id=candidate_id)
        candidate.status=settings.VIVIER_STATUS
        candidate.save()
    else:
        print("nothing to change")