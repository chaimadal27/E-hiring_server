# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# custom lib
from ..serializers import KeyWordsSerializer
from ..models import KeyWords


class KeyWordsCreateAPIView(ListCreateAPIView):
    serializer_class = KeyWordsSerializer
    permission_classes = [IsAuthenticated]
    queryset = KeyWords.objects.filter(
        deleted_at__isnull=True,
    )


class KeyWordsRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = KeyWordsSerializer
    permission_classes = [IsAuthenticated]
    queryset = KeyWords.objects.filter(
        deleted_at__isnull=True,
    )

class  AllKeyWordsList(generics.ListAPIView):
    queryset = KeyWords.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = KeyWordsSerializer
    pagination_class = None