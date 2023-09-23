# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import Candidate,LanguageDetail,KeyWords,Document
from .language_detail_serializer import LanguageDetailSerializer
from .document_serializer import DocumentSerializer


class CandidateSerializer(serializers.ModelSerializer):
  # languagedetail_set = LanguageDetailSerializer(many=True)
  #   document_set = DocumentSerializer(many=True)

    class Meta:
        model = Candidate
        fields = [
            'source',
            'rating',
            'linkedin_link',
            'civility',
            'key_words',
            'first_name_fr',
            'last_name_fr',
            'status',
            'email',
            'birth_date',
            'first_phone',
            'second_phone',
            'address',
            'postal_code',
            'city',
            'country',
            'family_situation',
            'education_level',
            'school',
            'speciality',
            'function',
            'first_employment_date',
            'seniority',
            'current_employer',
            'contract_type',
            'current_salary',
            'current_devise',
            'current_benefits',
            'desired_salary',
            'desired_devise',
            'disponibility',
            'years_of_experience',
            'mobility',
            #'languagedetail_set',
            #'document_set',
            'comment',
            'is_active',
            'id'
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user

      #  document_data = validated_data.pop('document_set')
        candidate = Candidate.objects.create(**validated_data)

        # save documents

        # for document in document_data:
        #     Document.objects.create(candidate=candidate, **document)
        # save key words
        key_words_data = validated_data.pop('key_words')
        for key_word in key_words_data:
            if (KeyWords.objects.filter(value=key_word).exists()):
                pass
            else:
                KeyWords.objects.create(value=key_word)
        return candidate

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        # documents_data = validated_data.pop('document_set')
        # documents = instance.document_set.all()
        # documents = list(documents)
        instance = super().update(instance, validated_data)

        # save documents
        # for document_data in documents_data:
        #     if documents:
        #         document = documents.pop(0)
        #         document.name = document_data.get('name')
        #         document.type = document_data.get('type')
        #         document.file = document_data.get('file')
        #         document.is_valid = document_data.get('is_valid')
        #         document.save()
        #     else:
        #         Document.objects.create(candidate=instance, **document_data)
        # save key words
        key_words_data = validated_data.pop('key_words')
        for key_word in key_words_data:
            if KeyWords.objects.filter(value=key_word).exists():
                pass
            else:
                KeyWords.objects.create(value=key_word)
        return instance

class CandidateKanbanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = [
            'source',
            'civility',
            'first_name_fr',
            'last_name_fr',
            'status',
            'email',
            'first_phone',
            'function',
            'disponibility',
            'id'
        ]

        read_only_fields = ['id']

class ShareCVSerializer(serializers.Serializer):
    recruiters = serializers.ListField()

    def create(self, validated_data):
        current_user = self.context.get('request').user
