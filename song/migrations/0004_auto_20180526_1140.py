# Generated by Django 2.0.5 on 2018-05-26 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0003_auto_20180526_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_type',
            field=models.CharField(choices=[('liturgical', 'liturgical'), ('secular', 'secular'), ('na', 'na')], default='na', max_length=30),
        ),
    ]
