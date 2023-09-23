from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.module_loading import import_string

from .tokens import EncodeJWTToken
from .exceptions import AuthenticationFailed, ResetPasswordFailed
from .backends import CustomJWTBackend
from .settings import SETTINGS
from .models import UserDBConfig
from .send_mail import send_mail_on_frogot_password, send_mail_on_password_reset

User = get_user_model()

PermissionSerializer = import_string(SETTINGS.PERMISSIONS_SERIALIZER_CLASS)
UserSerializer = import_string(SETTINGS.USER_SERIALIZER_CLASS)


class SuccessLoginMixin():
    @classmethod
    def generate_token(cls, payload={}):
        encodeJWTToken = EncodeJWTToken(payload)
        return encodeJWTToken.encode()

    def get_all_permissions(self, db_name, user):
        try:
            return Permission.objects.using(db_name).filter(Q(user=user) | Q(group__user=user)).distinct().all()
        except Permission.DoesNotExist:
            return []

    def after_success_authentication(self, user, db_name):
        payload = {
            SETTINGS.USER_ID_CLAIM: getattr(user, SETTINGS.USER_ID_FIELD),
            SETTINGS.DB_NAME_CLAIM: db_name
        }

        access_token = UserLoginSerializer.generate_token(payload)
        all_permissions = self.get_all_permissions(db_name, user)

        data = {}
        data['access'] = str(access_token)
        data['user'] = UserSerializer(user).data
        data['permissions'] = PermissionSerializer(all_permissions, many=True).data

        return data


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class UserLoginSerializer(SuccessLoginMixin, serializers.Serializer):
    auth_unique_field = SETTINGS.AUTH_UNIQUE_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.backend = CustomJWTBackend()
        self.fields[self.auth_unique_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        request = self.context['request']
        authenticate_kwargs = {
            self.auth_unique_field: attrs[self.auth_unique_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = request
        except KeyError:
            pass

        self.user = self.backend.authenticate(**authenticate_kwargs)

        if not self.user:
            raise AuthenticationFailed()

        return self.after_success_authentication(self.user, request.session[SETTINGS.DB_NAME_CLAIM])


class ResetPasswordSerializer(SuccessLoginMixin, serializers.Serializer):
    password = PasswordField(max_length=100)
    token = PasswordField(max_length=32)

    def validate(self, data):
        new_password = data.get('password')
        token = data.get('token')

        if token and new_password:
            try:
                (db_config_id, user_id) = User.decode_generated_token(token)
                db_config = UserDBConfig.objects.using('default').get(pk=db_config_id)
            except UserDBConfig.DoesNotExist:
                pass
            else:
                try:
                    queryset = User.objects.using(db_config.db_name).filter(**{SETTINGS.USER_ID_FIELD: user_id})
                    user = queryset.get()
                    if user and user.is_confirm_token_expired():
                        queryset.update(confirm_token=None, confirm_token_expired_at=None,
                                        password=make_password(new_password))
                        send_mail_on_password_reset(user)
                        return self.after_success_authentication(user, db_config.db_name)
                except User.DoesNotExist:
                    pass

        raise ResetPasswordFailed()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate(self, data):
        email = data.get('email')
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(email)
        pp.pprint('**********************************')
        if email:
            try:
                db_config = UserDBConfig.objects.using('default').get(auth_field=email)
                import pprint
                pp = pprint.PrettyPrinter(depth=6)
                pp.pprint('**********************************')
                pp.pprint(db_config)
                pp.pprint('**********************************')
            except UserDBConfig.DoesNotExist:
                pass
            else:
                try:

                    user = User.objects.using(db_config.db_name).filter(**{SETTINGS.AUTH_UNIQUE_FIELD: email}).get()
                    import pprint
                    pp = pprint.PrettyPrinter(depth=6)
                    pp.pprint('**********************************')
                    pp.pprint(user)
                    pp.pprint('**********************************')
                    if user:
                        user.generate_token(db_config.id)
                        user.save(using=db_config.db_name)
                        send_mail_on_frogot_password(user)
                except User.DoesNotExist:
                    pass

        return []
