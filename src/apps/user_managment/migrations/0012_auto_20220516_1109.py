# Generated by Django 3.1 on 2022-05-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_state', '0001_initial'),
        ('user_managment', '0011_auto_20220516_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_state',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_state',
            field=models.ManyToManyField(to='resource_state.ResourceState'),
        ),
    ]
