# Generated by Django 2.1.3 on 2018-11-24 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20181124_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='invitations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.GameInvitation'),
        ),
    ]
