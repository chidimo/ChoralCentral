# Generated by Django 2.0.1 on 2018-02-06 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='song',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song'),
        ),
    ]
