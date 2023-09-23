from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.conf import settings

from ...models.activity import Activity
from ...models.activity_type import ActivityType

from django.db import connection


class Command(BaseCommand):
    help = 'tell me why tell me why'
    def add_arguments(self, parser):
        parser.add_argument('-db','--database',type=str, help="Define the database.")

    def handle(self, *args, **kwargs):
        db_name  = kwargs['database']

        if not db_name:
            raise CommandError("You need the specify which database")

        try:
            for default_activity_type in settings.ACTIVITY_TYPE:
                print("---------------------------------------------------")
                print(default_activity_type)
                print("---------------------------------------------------")
                activity_type = ActivityType.objects.using(db_name).filter(activity_type_name=['activity_type_name']).first()
                if not activity_type:
                    activity_type = ActivityType(activity_type_name=default_activity_type["activity_type_name"])
                    activity_type.save(using=db_name)
            self.stdout.write(self.style.SUCCESS('FINALLY, ACTIVITY TYPE CREATED SUCCESSFULLY'))

        

        except IntegrityError as err:
            raise CommandError(str(err))


        try:
            for default_activity in settings.ACTIVITY:
                print('****************************************************')
                print(default_activity['activity_type'])
                print('****************************************************')
        except IntegrityError as err:
            raise CommandError(str(err))
