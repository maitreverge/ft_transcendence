# Generated by Django 5.1.7 on 2025-03-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseapi_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
