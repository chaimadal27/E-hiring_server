# Generated by Django 3.1 on 2021-04-01 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_managment', '0003_auto_20210401_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]