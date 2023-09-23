from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'apps.jwt_authentication'
    label = 'jwt_authentication'

    # def ready(self):
    #     import apps.jwt_authentication.signals
