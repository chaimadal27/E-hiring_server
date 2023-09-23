from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.conf import settings
from apps.lists_managment.models import List
from django.db import connection

class Command(BaseCommand):
    help = 'Create immutable object'

    def add_arguments(self, parser):
        parser.add_argument('-db', '--database', type=str, help="Define the database.")

    def handle(self, *args, **kwargs):
        # cursor = connection.cursor()
        # sql = ".tables;"
        # cursor.execute(sql)
        db_name = kwargs['database']
        if not db_name:
            raise CommandError("Hey! You must set the database name")
        #Groups and permissions creation
        try:
            for default_group in settings.IMMUTABLE_GROUPS:
                group = Group.objects.using(db_name).filter(name=default_group["name"]).first()

                if not group:
                    group = Group(name=default_group["name"])
                    group.save(using=db_name)

                permissions = Permission.objects.using(db_name).filter(
                    codename__in=default_group["permissions"]
                ).values_list('id', flat=True)

                # permissions and group.permissions.set(permissions)
                group.save(using=db_name)
            self.stdout.write(self.style.SUCCESS('Good Job! The groups has been created Successfully'))
        except IntegrityError as err:
            raise CommandError(str(err))
        #Lists creation
        try:
            for default_list in settings.IMMUTABLE_LISTS:
                list = List.objects.using(db_name).filter(name=default_list["name"]).first()

                if not list:
                    list = List(name=default_list["name"])
                    list.save(using=db_name)

            self.stdout.write(self.style.SUCCESS('Good Job! The lists has been created Successfully'))
        except IntegrityError as err:
            raise CommandError(str(err))

