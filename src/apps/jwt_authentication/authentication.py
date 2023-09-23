from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication
from django.contrib.auth import get_user_model

from .settings import SETTINGS
from .mixins import GetTokenFromRequestHeaderMixin
from .exceptions import InvalidToken, TokenError, AuthenticationFailed

UserModel = get_user_model()


class CustomJWTAuthentication(authentication.BaseAuthentication, GetTokenFromRequestHeaderMixin):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            SETTINGS.AUTH_HEADER_TYPE_BYTES[0],
            self.www_authenticate_realm,
        )
 
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[SETTINGS.USER_ID_CLAIM]
            db_name = validated_token[SETTINGS.DB_NAME_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = UserModel.objects.using(db_name).get(**{SETTINGS.USER_ID_FIELD: user_id})
        except UserModel.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user
