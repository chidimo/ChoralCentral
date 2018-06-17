# Generated by Django 2.0.5 on 2018-06-17 23:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='Not set', message='Only alphanumeric values are allowed.', regex='[a-zA-Z-\\s]+')]),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='Not set', message='Only alphanumeric values are allowed.', regex='[a-zA-Z-\\s]+')]),
        ),
    ]
