# Generated by Django 3.1 on 2021-03-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel_managment', '0002_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='school',
            name='short_name_ar',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]