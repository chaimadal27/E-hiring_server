# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status, serializers
# custom lib
from ..models import LanguageDetail, Candidate
from ..serializers.candidate_language_serializer import CandidateLanguageSerializer
from ..serializers.candidate_Document_serializer import CandidateDocumentSerializer

class CandidateDocumentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CandidateDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()


class CandidateDocumentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )


