# Generated by Django 5.1.6 on 2025-02-24 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserManagementDummyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_dummy', models.CharField(max_length=100)),
                ('name_dummy_2', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'user_schema.usermanagementdummymodel',
            },
        ),
    ]
