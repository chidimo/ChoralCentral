# Generated by Django 2.0.5 on 2018-05-22 21:36

from django.db import migrations, models
import universal.media_handlers


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='midi',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to=universal.media_handlers.save_midi),
        ),
        migrations.AlterField(
            model_name='score',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to=universal.media_handlers.save_score),
        ),
    ]