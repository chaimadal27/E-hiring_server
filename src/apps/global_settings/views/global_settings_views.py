from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models.global_settings_model import GlobalSettings
from ..serializers.global_settings_serializer import GlobalSettingsSerializer

class GlobalSettingsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer


class GlobalSettingsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer