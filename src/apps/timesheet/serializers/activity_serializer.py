from rest_framework import serializers
from ..models.activity import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id','activity_name','activity_type']
        read_only_fields = ['id']
