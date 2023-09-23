from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication
from .settings import SETTINGS
from .exceptions import InvalidToken, TokenError, AuthenticationFailed
from .tokens import DecodeJWTToken


class GetTokenFromRequestHeaderMixin:

    def get_db_name_from_session(self, request):
        try:
            return request.session[SETTINGS.DB_NAME_CLAIM]
        except KeyError:
            return None

    def get_db_name_from_header(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        try:
            return validated_token[SETTINGS.DB_NAME_CLAIM]
        except KeyError:
            None

    def get_db_name(self, request):
        """
        Attempts to find and return the database name for the current user.
        """
        db_name = self.get_db_name_from_session(request)
        if db_name is None:
            db_name = self.get_db_name_from_header(request)
        return db_name

    
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(SETTINGS.AUTH_HEADER_NAME)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in SETTINGS.AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        try:
            decode_token = DecodeJWTToken(raw_token)
            return decode_token.decode(raw_token, verify=True)
        except TokenError as e:
            messages.append({'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })
