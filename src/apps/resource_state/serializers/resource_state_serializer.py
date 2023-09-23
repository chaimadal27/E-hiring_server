from rest_framework import serializers
from ..models.resource_state_model import ResourceState

class ResourceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceState
        fields = ['id','resource_state']
   
    
