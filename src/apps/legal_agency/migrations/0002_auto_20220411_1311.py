# Generated by Django 3.1 on 2022-04-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal_agency', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legalagency',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='legalagency',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]