# Generated by Django 2.0.1 on 2018-04-25 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolink',
            name='youtube_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videolink',
            name='youtube_views',
            field=models.IntegerField(default=0),
        ),
    ]
