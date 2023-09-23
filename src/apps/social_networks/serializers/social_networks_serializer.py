from rest_framework import serializers
from ..models.social_network_model import SocialNetwork


class SocialNetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('id','social_network_link','user')


         