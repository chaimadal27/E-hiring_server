from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Exists, OuterRef, Q
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login


from .settings import SETTINGS
from .models import UserDBConfig
from .exceptions import InvalidToken, TokenError, AuthenticationFailed


UserModel = get_user_model()
user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')


class CustomJWTBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            username = kwargs.get(SETTINGS.AUTH_UNIQUE_FIELD)
        
        if username is None or password is None:
            return

        if username and password:
            try:
                db_config = UserDBConfig.objects.using('default').get(auth_field=username)
            except UserDBConfig.DoesNotExist:
                return
            else:
                try:
                    user = UserModel._default_manager.using(db_config.db_name).get(**{ SETTINGS.AUTH_UNIQUE_FIELD: username})
                except UserModel.DoesNotExist:
                    # Run the default password hasher once to reduce the timing
                    # difference between an existing and a nonexistent user (#20760).
                    UserModel().set_password(password)
                else:
                    if user.check_password(password) and self.user_can_authenticate(user):
                        request.session[SETTINGS.DB_NAME_CLAIM] = db_config.db_name
                        return user
