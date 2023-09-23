# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

# custom lib
from ..serializers import LanguageDetailSerializer, CandidateLanguageSerializer
from ..models import LanguageDetail, Candidate


class LanguageDetailCreateAPIView(ListCreateAPIView):
    serializer_class = LanguageDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = LanguageDetail.objects.filter(
        deleted_at__isnull=True,
    )


class LanguageDetailRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CandidateLanguageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )