# Generated by Django 3.1 on 2021-03-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists_managment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='rank',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='value',
            field=models.CharField(blank=True, default='Ajouter une option ici...', max_length=200, null=True),
        ),
    ]
