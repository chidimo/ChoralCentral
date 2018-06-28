# Generated by Django 2.0.5 on 2018-06-28 21:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='Not set', message='Only alphabetic values are allowed.', regex='[a-zA-Z-\\s]+')])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='Not set', message='Only alphabetic values are allowed.', regex='[a-zA-Z-\\s]+')])),
                ('bio', models.TextField(blank=True, null=True)),
                ('slug', universal.fields.AutoMultipleSlugField(blank=True, editable=False, max_length=255, set_once=True, set_using=['last_name', 'first_name'])),
                ('author_type', models.CharField(choices=[('', 'Select author type'), ('lyricist', 'Lyricist'), ('composer', 'Composer'), ('lyricist and composer', 'Lyricist and Composer')], max_length=25)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('last_name', '-created'),
            },
        ),
    ]
