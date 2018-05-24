# Generated by Django 2.0.5 on 2018-05-24 08:49

from django.db import migrations, models
import universal.media_handlers


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0005_auto_20180524_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='media_file',
            field=models.FileField(null=True, upload_to=universal.media_handlers.save_score),
        ),
    ]
