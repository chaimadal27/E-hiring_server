# Generated by Django 3.1 on 2022-05-17 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0003_auto_20220516_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sheet',
            options={'permissions': [('validate_sheet', 'Can validate timesheet'), ('invalidate_sheet', 'Can invalidate timesheet')]},
        ),
    ]
