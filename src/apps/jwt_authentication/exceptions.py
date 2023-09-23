from rest_framework import exceptions, status


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication failed'
    default_code = 1100


class InvalidToken(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token is invalid or expired'
    default_code = 1101


class TokenError(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is invalid or expired'
    default_code = 1102


class ResetPasswordFailed(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Reset password failed'
    default_code = 1103


class InvalidUserIdentifier(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User identifier is already exists'
    default_code = 1104
