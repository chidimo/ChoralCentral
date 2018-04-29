# Generated by Django 2.0.1 on 2018-04-29 05:27

from django.db import migrations, models
import universal.media_handlers


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0004_midi_drive_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=universal.media_handlers.save_drive_pdf_thumbnail),
        ),
        migrations.AlterField(
            model_name='midi',
            name='drive_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='drive_url',
            field=models.URLField(null=True),
        ),
    ]
