# Generated by Django 2.0.1 on 2018-05-01 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0009_auto_20180501_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='midi',
            name='embed_link',
            field=models.URLField(null=True),
        ),
    ]
