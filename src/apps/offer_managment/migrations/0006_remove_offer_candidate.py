# Generated by Django 3.1 on 2021-05-31 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer_managment', '0005_auto_20210531_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='candidate',
        ),
    ]
