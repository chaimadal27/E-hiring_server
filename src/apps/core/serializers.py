from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.db.models import Q

from .models import User #, Address


class PermissionSerializer(serializers.ModelSerializer):
    #app = serializers.SerializerMethodField()
    #model = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = (
            'id',
            'codename',
        )

    def get_app(self, obj):
        return obj.content_type.app_label

    def get_model(self, obj):
        return obj.content_type.model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'first_name_ar',
            'last_name_ar',
            'email',
            'is_superuser',
        )

