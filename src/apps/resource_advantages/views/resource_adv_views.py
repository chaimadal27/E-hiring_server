from rest_framework import generics
from ..models.resource_advantages import ResourceAdvantages
from ..serializers.resource_advantages_serializer import ResourceAdvantagesSerializer


class ResourceAdvantagesList(generics.ListCreateAPIView):
    queryset = ResourceAdvantages.objects.all()
    serializer_class = ResourceAdvantagesSerializer


class ResourceAdvantagesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceAdvantages.objects.all()
    serializer_class = ResourceAdvantagesSerializer