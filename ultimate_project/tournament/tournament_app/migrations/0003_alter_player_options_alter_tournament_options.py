# Generated by Django 5.1.6 on 2025-02-25 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0002_match_player_tournament_delete_tournamentdummymodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.AlterModelOptions(
            name='tournament',
            options={'managed': False},
        ),
    ]
