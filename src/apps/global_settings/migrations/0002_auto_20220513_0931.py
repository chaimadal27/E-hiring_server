# Generated by Django 3.1 on 2022-05-13 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legal_agency', '0002_auto_20220411_1311'),
        ('global_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='is_global',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='legal_agency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='legal_agency.legalagency'),
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='setting_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]