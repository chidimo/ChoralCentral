# Generated by Django 2.0.5 on 2018-05-26 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0009_remove_song_first_line'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='song_type',
            new_name='ocassion',
        ),
    ]
