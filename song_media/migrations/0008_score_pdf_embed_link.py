# Generated by Django 2.0.1 on 2018-04-29 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_media', '0007_auto_20180429_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='pdf_embed_link',
            field=models.URLField(null=True),
        ),
    ]
