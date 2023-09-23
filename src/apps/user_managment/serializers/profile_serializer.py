from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers
from ...resource_state.models.resource_state_model import ResourceState
from ..models import Profile
from ..exceptions import WrongPasswordException
from .group_serializer import PermissionSerializer, GroupSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    display_permissions = serializers.SerializerMethodField()
    display_groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'first_name_ar',
            'last_name_ar',
            'email',
            'username',
            'is_superuser',
            'user_permissions',
            'display_permissions',
            'groups',
            'display_groups',

        )
        extra_kwargs = {
            'user_permissions': {'required': False},
            'groups': {'required': False},
        }
        read_only_fields = (
            'id',
            'display_permissions',
            'display_groups',
            'is_active'
        )

    def to_internal_value(self, data):
        permission_data = data.get('user_permissions', None)
        if not permission_data:
            data['user_permissions'] = []
        return data

    def get_display_permissions(self, obj):
        return PermissionSerializer(obj.user_permissions, many=True).data

    def get_user_permissions(self, obj):
        return obj.user_permissions.all().values_list('codename', flat=True)

    def get_display_groups(self, obj):
        return GroupSerializer(obj.groups, many=True).data


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser'

        )
        read_only_fields = (
            'id',
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'id',
            'civility',
            'phone',
            'second_phone',
            'user',
            'is_active',
            'is_deleted',
            'other_emails',
            'user_dob',
            'user_city',
            'user_postal_code',
            'user_country',
            'tjm',
            'devise',
            'mobility',
            # 'business_unit',
            'user_state',
            'is_manager',


        )
        extra_kwargs = {
            'user': {'required': True},
        }
        read_only_fields = (
            'id',
            'is_active',
            'is_deleted',

        )

    def create(self, validated_data):
        current_user = self.context.get('request').user
        created_by = current_user
        user_data = validated_data.pop('user')
        permission_data = user_data.pop('user_permissions', None)
        groups_data = user_data.pop('groups', None)
        user = User(**user_data, is_active=True)
        user.save()
        if permission_data:
            permissions = Permission.objects.filter(
                codename__in=permission_data).all()
            user.user_permissions.set(permissions)
        if groups_data:
            user.set_groups(groups_data)
        profile = Profile.objects.create(
            user=user,
            created_by=created_by,
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        context_user = self.context.get('request')
        print("++++++++++++++++++++++++++++++++")
        print(context_user)
        print("++++++++++++++++++++++++++++++++")
        # updated_by = current_user
        instance.civility = validated_data.get('civility', instance.civility)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.second_phone = validated_data.get(
            'second_phone', instance.second_phone)
        instance.is_deleted = validated_data.get(
            'is_deleted', instance.is_deleted)
        instance.other_emails = validated_data.get(
            'other_emails', instance.other_emails)
        instance.user_dob = validated_data.get('user_dob', instance.user_dob)
        instance.user_city = validated_data.get(
            'user_city', instance.user_city)
        instance.user_postal_code = validated_data.get(
            'user_postal_code', instance.user_postal_code)
        instance.user_country = validated_data.get(
            'user_country', instance.user_country)
        instance.tjm = validated_data.get('tjm', instance.tjm)
        instance.devise = validated_data.get('devise', instance.devise)
        instance.mobility = validated_data.get('mobility', instance.mobility)
        instance.user_state = validated_data.get(
            'user_state', instance.user_state)
        instance.is_manager = validated_data.get(
            'is_manager', instance.is_manager)
        user_data = validated_data.pop('user', None)
        user = instance.user
        if user_data:
            user.first_name_ar = user_data.get(
                'first_name_ar', user.first_name_ar)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.last_name_ar = user_data.get(
                'last_name_ar', user.last_name_ar)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)

        permission_data = user_data.get(
            'user_permissions', instance.user.user_permissions)
        if permission_data:
            user.user_permissions.set(Permission.objects.filter(
                codename__in=permission_data).all())

        groups_data = user_data.get('groups', instance.user.groups)
        if groups_data:
            user.groups.set(groups_data)

        instance.save()
        user.save()

        return instance

        # if user_data:
        #     user.first_name_ar = user_data.get('first_name_ar', user.first_name_ar)
        #     user.first_name = user_data.get('first_name', user.first_name)
        #     user.last_name_ar = user_data.get('last_name_ar', user.last_name_ar)
        #     user.last_name = user_data.get('last_name', user.last_name)
        #     user.username = user_data.get('username', user.username)
        #     user.email = user_data.get('email', user.email)
        #     user.is_superuser = user_data.get('is_superuser', user.is_superuser)
        #     user.is_active = user_data.get('is_active', user.is_active)
        #     user.is_staff = user_data.get('is_staff', user.is_staff)
        # permission_data = user_data.get('user_permissions', instance.user.user_permissions)
        # if permission_data:
        #     user.user_permission.set(Permission.objects.filter(codename__in=permission_data).all())
        # group_data = user_data.get('groups', instance.user.groups)
        # if group_data:
        #     user.groups.set(group_data)
        # # instance.save(updated_by)
        # user.save()
        # return instance


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'first_name_ar',
            'last_name_ar',
            'email',
            'is_superuser'
        )


class CurrentProfileSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer()
    current_password = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = (
            'civility',
            'phone',
            'second_phone',
            'user',
            'current_password'
        )
        extra_kwargs = {
            'user': {'required': True}, 'current_password': {'write_only': True},
            'civility': {'read_only': True}
        }
        read_only_fields = (
            'civility',
        )

    def validate(self, attrs):
        current_user = self.context.get('request').user
        current_password = attrs.get('current_password')

        if not current_user.check_password(current_password):
            raise WrongPasswordException('Wrong password.')

        return super().validate(attrs)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        instance.civility = validated_data.get('civility', instance.civility)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.second_phone = validated_data.get(
            'second_phone', instance.second_phone)

        user_data = validated_data.pop('user', None)
        user = instance.user
        if user_data:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.first_name_ar = user_data.get(
                'first_name_ar', user.first_name_ar)
            user.last_name_ar = user_data.get(
                'last_name_ar', user.last_name_ar)
            user.username = user_data.get('username', user.username)
            new_email = user_data.get('email', user.email)

        instance.save()
        user.save()

        return instance


class UpdateCurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)

    def validate(self, data):
        current_user = self.context.get('request').user
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_user.check_password(current_password):
            raise WrongPasswordException('Wrong password.')
        current_user.set_password(new_password)
        current_user.save()

        return data
