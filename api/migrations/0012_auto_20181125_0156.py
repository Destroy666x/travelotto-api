# Generated by Django 2.1.3 on 2018-11-25 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20181125_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lottery',
            name='games',
        ),
        migrations.AddField(
            model_name='lottery',
            name='games',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
    ]
