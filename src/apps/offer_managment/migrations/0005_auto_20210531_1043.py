# Generated by Django 3.1 on 2021-05-31 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_managment', '0013_auto_20210531_1043'),
        ('offer_managment', '0004_kanban'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='kanban',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate_managment.candidate'),
        ),
        migrations.AlterUniqueTogether(
            name='kanban',
            unique_together={('candidate', 'offer')},
        ),
    ]
