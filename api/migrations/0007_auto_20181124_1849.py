# Generated by Django 2.1.3 on 2018-11-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20181124_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamequestion',
            name='game',
        ),
        migrations.AddField(
            model_name='game',
            name='questions',
            field=models.ManyToManyField(related_name='questions', to='api.GameQuestion'),
        ),
    ]
