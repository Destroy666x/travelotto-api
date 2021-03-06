# Generated by Django 2.1.3 on 2018-11-25 03:11

import api.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20181125_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamelocation',
            name='status',
            field=models.CharField(choices=[('TO_VISIT', 'TO_VISIT'), ('VISITED_CORRECTLY', 'VISITED_CORRECTLY'), ('VISITED_INCORRECTLY', 'VISITED_INCORRECTLY')], default=api.enums.GameLocationStatus('TO_VISIT'), max_length=30),
        ),
        migrations.AddField(
            model_name='location',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
