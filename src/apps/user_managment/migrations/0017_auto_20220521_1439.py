# Generated by Django 3.1 on 2022-05-21 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managment', '0016_auto_20220518_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]