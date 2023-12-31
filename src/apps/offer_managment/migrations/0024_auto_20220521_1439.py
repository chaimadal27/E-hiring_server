# Generated by Django 3.1 on 2022-05-21 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_managment', '0023_auto_20220514_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='kanban',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='kanban',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
