# Generated by Django 5.1.7 on 2025-03-24 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseapi_app', '0002_remove_player_two_fa_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='two_fa_verified',
            field=models.BooleanField(default=False),
        ),
    ]
