from rest_framework import exceptions, status

from apps.core.mixins import ExceptionMixin


class UnauthorizedUpdateException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'You are unauthorized to update'
    default_reason = 'Reason'
    default_code = 1303


class ServiceRelationException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Cannot delete this service'
    default_reason = 'Reason'
    default_code = 1304
