from rest_framework import exceptions, status

from apps.core.mixins import ExceptionMixin


class DuplicateValuesException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Duplicated Data'
    default_reason = 'Reason'
    default_code = 1302
