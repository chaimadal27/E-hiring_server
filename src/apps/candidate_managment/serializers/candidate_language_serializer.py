# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import Candidate,LanguageDetail
from .language_detail_serializer import LanguageDetailSerializer
from .document_serializer import DocumentSerializer

class CandidateLanguageSerializer(serializers.ModelSerializer):
    languagedetail_set = LanguageDetailSerializer(many=True)

    class Meta:
        model = Candidate
        fields = [
            'languagedetail_set',
            'id'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        language_details_data = validated_data.pop('languagedetail_set')
        candidate_language = Candidate.objects.create(**validated_data)
        for language_detail in language_details_data:
            LanguageDetail.objects.create(candidate_language=candidate_language, **language_detail)
        return candidate_language

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        print("************************* 37 *********************")
        language_details_data = validated_data.pop('languagedetail_set')
        language_details = instance.languagedetail_set.all()
        language_details = list(language_details)
        instance = super().update(instance, validated_data)
        for language_detail_data in language_details_data:
            if language_details:
                language_detail = language_details.pop(0)
                language_detail.language = language_detail_data.get('language')
                language_detail.level = language_detail_data.get('level')
                language_detail.save()
            else:
                print("***************** 49 *********************")
                LanguageDetail.objects.create(candidate=instance, **language_detail_data)

        return instance



