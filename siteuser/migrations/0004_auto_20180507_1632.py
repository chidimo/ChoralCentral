# Generated by Django 2.0.1 on 2018-05-07 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0003_siteuser_used'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteuser',
            old_name='used',
            new_name='remaining',
        ),
    ]