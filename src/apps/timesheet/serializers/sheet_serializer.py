from rest_framework import serializers
from ..models.sheet import Sheet

class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = ('id','coef','user')


    def create(self, validated_data):
        current_user = self.context.get('request').user