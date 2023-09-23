from .user_db_config import UserDBConfig
from ..exceptions import InvalidUserIdentifier
from ..settings import SETTINGS

from ..send_mail import send_mail_on_create_new_account, send_mail_on_update_account


def update_db_config_pre_save(sender, instance=None, using='default', **kwargs):
    if instance.is_superuser:
        pass
        #return

    auth_unique_field = instance and getattr(instance, SETTINGS.AUTH_UNIQUE_FIELD)
    user_unique_field = instance and getattr(instance, SETTINGS.USER_ID_FIELD)
    created = not bool(user_unique_field)
    unique_field = auth_unique_field and "{0}__{1}".format(using, user_unique_field or auth_unique_field)

    if not created and user_unique_field:
        UserDBConfig.objects.using('default').filter(
            auth_field=auth_unique_field
        ).update(
            unique_config=unique_field
        )

    # unique validation
    try:
        user_db_config = UserDBConfig.objects.using('default').filter(auth_field=auth_unique_field).get()
        if (user_db_config and created) or \
                (user_db_config and not created and user_db_config.unique_config != unique_field):
            return
    except UserDBConfig.DoesNotExist:
        pass

    # update the db config
    if created:
        db_config = UserDBConfig.objects.using('default').create(
            unique_config=unique_field,
            db_name=using,
            auth_field=auth_unique_field
        )
        # print(db_config)
        # setattr(instance, SETTINGS.DB_NAME_CLAIM, db_config)
    else:
        UserDBConfig.objects.using('default').filter(
            unique_config=unique_field
        ).update(
            auth_field=auth_unique_field
        )


def update_db_config_post_save(sender, instance=None, using='default', created=True, **kwargs):
    if created:
        auth_unique_field = getattr(instance, SETTINGS.AUTH_UNIQUE_FIELD)
        try:
            db_config = getattr(instance, SETTINGS.DB_NAME_CLAIM, None)
            if db_config is None:
                db_config = UserDBConfig.objects.using('default').get(auth_field=auth_unique_field)
        except UserDBConfig.DoesNotExist:
            pass
        else:
            instance.generate_token(db_config.id)
            instance.save(using=using)
            send_mail_on_create_new_account(instance)

    else:
        send_mail_on_update_account(instance)

