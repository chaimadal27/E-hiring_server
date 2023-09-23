from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from ...models import UserDBConfig
from ...send_mail import send_mail_on_create_new_account


class Command(BaseCommand):
    help = 'Create super user'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help="Define an admin's name.")
        parser.add_argument('-e', '--email', type=str, help="Define an admin's email.")
        parser.add_argument('-w', '--password', type=str, help="Define an admin's password.")
        parser.add_argument('-c', '--civility', type=int, help="Define a database")
        parser.add_argument('-P', '--phone', type=str, help="Define a database")
        parser.add_argument('-S', '--second-phone', type=str, help="Define a database")
        parser.add_argument('-f', '--firstname', type=str, help="Define a database")
        parser.add_argument('-F', '--firstname_ar', type=str, help="Define a database")
        parser.add_argument('-l', '--lastname', type=str, help="Define a database")
        parser.add_argument('-L', '--lastname_ar', type=str, help="Define a database")
        parser.add_argument('-d', '--database', type=str, help="Define a database")

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        firstname = kwargs['firstname']
        firstname_ar = kwargs['firstname_ar']
        lastname = kwargs['lastname']
        lastname_ar = kwargs['lastname_ar']
        civility = kwargs['civility']
        phone = kwargs['phone']
        second_phone = kwargs.get('second-phone', '')
        email = kwargs['email']
        database = kwargs.get('database', 'default')
        password = kwargs.get('password', None)
        try:
            if UserDBConfig.objects.using('default').filter(db_name=database, auth_field=email).exists():
                self.stdout.write(self.style.WARNING('Oh snap! The super user has been already created'))
                return

            User = get_user_model()
            Profile = User.profile.related.related_model
            user = User(
                username=username,
                email=email,
                is_superuser=True,
                first_name=firstname,
                last_name=lastname,
                first_name_ar=firstname_ar,
                last_name_ar=lastname_ar
            )
            if password:
                user.set_password(password)
            user.save(using=database)
            Profile.objects.using(database).create(
                user=user,
                created_by=user,
                phone=phone,
                second_phone=second_phone,
                civility=civility
            )
            db_config = UserDBConfig.objects.using('default').create(unique_config='{}__{}'.format(user.id, user.email), db_name=database, auth_field=user.email)
            user.generate_token(db_config.id)
            user.save(using=database)
            send_mail_on_create_new_account(user)

            self.stdout.write(self.style.SUCCESS('Good Job! The super user has been created Successfully'))
        except IntegrityError as e:
            raise CommandError('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
