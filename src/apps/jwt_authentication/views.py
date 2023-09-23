from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import get_user_model

from .send_mail import send_mail_on_frogot_password
from .settings import SETTINGS
from .exceptions import TokenError, InvalidToken
from .serializers import UserLoginSerializer, ResetPasswordSerializer, ForgotPasswordSerializer

User = get_user_model()


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            SETTINGS.AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'kwargs': kwargs})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if serializer.validated_data:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordAPIView(TokenViewBase):
    serializer_class = ForgotPasswordSerializer

class ResetPasswordAPIView(TokenViewBase):
    serializer_class = ResetPasswordSerializer

class JWTLoginView(TokenViewBase):
    serializer_class = UserLoginSerializer
