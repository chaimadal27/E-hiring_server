# Generated by Django 3.1 on 2022-04-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managment', '0002_auto_20201110_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='devise',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobility',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tjm',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_first_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_last_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_postal_code',
            field=models.IntegerField(null=True),
        ),
    ]