# Generated by Django 5.1.7 on 2025-03-17 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databaseapi_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='two_fa_verified',
        ),
    ]
