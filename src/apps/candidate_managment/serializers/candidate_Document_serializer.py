# python lib
import datetime
from django.db.models import Q
# django lib
from rest_framework import serializers

# custom lib
from ..models import Candidate,LanguageDetail,Document
from .language_detail_serializer import LanguageDetailSerializer
from .document_serializer import DocumentSerializer

class CandidateDocumentSerializer(serializers.ModelSerializer):
    document_set = DocumentSerializer(many=True)
    class Meta:
        model = Candidate
        fields = [
            'document_set',
            'id',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        document_data = validated_data.pop('document_set')
        candidate_document = Candidate.objects.create(**validated_data)
        for document in document_data:
            Document.objects.create(candidate_document=candidate_document, **document)
        return candidate_document

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        print("************************* 38 *********************")
        documents_data = validated_data.pop('document_set')
        documents = instance.document_set.all()
        documents = list(documents)
        instance = super().update(instance, validated_data)
        for document_data in documents_data:
            if documents:
                document = documents.pop(0)
                document.name = document_data.get('name')
                document.type = document_data.get('type')
                document.file = document_data.get('file')
                document.is_valid = document_data.get('is_valid')
                document.save()
            else:
                print("************************* 50 *********************")
                Document.objects.create(candidate=instance, **document_data)
        return instance



