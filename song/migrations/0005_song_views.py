# Generated by Django 2.0.1 on 2018-02-28 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0004_auto_20180228_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='views',
            field=models.IntegerField(default=1),
        ),
    ]