# Generated by Django 2.0.1 on 2018-02-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_song_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='like_count',
            field=models.IntegerField(default=1),
        ),
    ]