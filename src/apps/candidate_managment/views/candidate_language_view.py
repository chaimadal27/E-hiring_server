# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status, serializers
# custom lib
from ..models import LanguageDetail, Candidate
from ..serializers.candidate_language_serializer import CandidateLanguageSerializer


class CandidateLanguageCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CandidateLanguageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()


class CandidateLanguageRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateLanguageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )


