# Generated by Django 2.0.5 on 2018-06-12 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_auto_20180611_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_type',
            field=models.CharField(choices=[('', 'Select author type'), ('lyricist', 'Lyricist'), ('composer', 'Composer'), ('lyricist and composer', 'Lyricist and Composer')], default='lyricist', max_length=15),
        ),
    ]