# Generated by Django 3.1 on 2022-03-04 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel_managment', '0008_auto_20210416_1727'),
        ('candidate_managment', '0018_remove_document_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='referentiel_managment.school'),
        ),
    ]
