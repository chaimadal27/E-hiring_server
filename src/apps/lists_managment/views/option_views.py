# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters

# custom lib
from ..serializers import OptionSerializer
from ..models import Option,List


class OptionCreateAPIView(ListCreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Option.objects.filter(
        deleted_at__isnull=True,
    )

class  AllOptionsBylistList(generics.ListAPIView):
    queryset = Option.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = OptionSerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        name = self.request.query_params.get('name')
        list = List.objects.get(name=name)
        return queryset.filter(list=list)

class OptionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Option.objects.filter(
        deleted_at__isnull=True,
    )
