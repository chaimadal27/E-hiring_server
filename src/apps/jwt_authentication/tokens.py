import datetime
import jwt
from .exceptions import TokenError
from .settings import SETTINGS


class EncodeJWTToken:

    def __init__(self, payload = {}):
        self.payload = payload

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def encode(self):
        """
        Returns an encoded token for the given payload dictionary.
        """
        jwt_payload = self.payload.copy()
        token = jwt.encode(jwt_payload, SETTINGS.SIGNING_KEY, SETTINGS.ALGORITHM)
        return token.decode('utf-8')


class DecodeJWTToken:

    def __init__(self, token):
        self.token = token


    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.
        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        try:
            return jwt.decode(token, SETTINGS.SIGNING_KEY, algorithms=[SETTINGS.ALGORITHM], verify=True)
        except jwt.InvalidAlgorithmError as ex:
            raise TokenError('Invalid algorithm specified')
        except jwt.InvalidTokenError:
            raise TokenError('Token is invalid or expired')
