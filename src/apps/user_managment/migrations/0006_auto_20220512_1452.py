# Generated by Django 3.1 on 2022-05-12 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_state', '0001_initial'),
        ('user_managment', '0005_auto_20220420_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='devise',
            field=models.CharField(default='euro', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobility',
            field=models.CharField(default='anywhere', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tjm',
            field=models.DecimalField(decimal_places=2, default=1.2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_city',
            field=models.CharField(default='Gafsa', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_country',
            field=models.CharField(default='Tunisie', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_dob',
            field=models.DateField(default='10/05/1998', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_postal_code',
            field=models.IntegerField(default=2100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_state',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='resource_state.resourcestate'),
        ),
    ]
