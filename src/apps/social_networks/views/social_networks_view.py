from rest_framework import generics
from ..models.social_network_model import SocialNetwork
from ..serializers.social_networks_serializer import SocialNetworksSerializer


class SocialNetworkList(generics.ListCreateAPIView):
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworksSerializer


class SocialNetworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworksSerializer