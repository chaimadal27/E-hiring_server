# Generated by Django 3.1 on 2022-05-12 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='can_access_canidates',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='can_access_resources',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='can_validate_timesheet',
            field=models.BooleanField(default=False, null=True),
        ),
    ]