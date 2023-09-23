from .user_db_config import UserDBConfig

from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from .signals import update_db_config_pre_save, update_db_config_post_save

UserModel = get_user_model()
pre_save.connect(update_db_config_pre_save, sender=UserModel)
post_save.connect(update_db_config_post_save, sender=UserModel)
