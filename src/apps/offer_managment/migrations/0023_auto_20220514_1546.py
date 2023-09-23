# Generated by Django 3.1 on 2022-05-14 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer_managment', '0022_auto_20220514_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='recruiter',
            field=models.ManyToManyField(blank=True, null=True, related_name='recruiter', to=settings.AUTH_USER_MODEL),
        ),
    ]