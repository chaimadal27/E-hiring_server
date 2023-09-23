# Generated by Django 3.1 on 2022-04-11 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('legal_agency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_unit_name', models.CharField(max_length=50)),
                ('legal_agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legal_agency.legalagency')),
            ],
        ),
    ]