# Generated by Django 2.0.6 on 2018-07-01 01:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0001_initial'),
        ('author', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MassPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('about', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('about', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('publish', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2018)])),
                ('slug', universal.fields.AutoSlugField(blank=True, editable=False, max_length=255, set_once=False, set_using='title')),
                ('lyrics', models.TextField(blank=True)),
                ('scripture_reference', models.CharField(blank=True, max_length=25)),
                ('tempo', models.IntegerField(blank=True, null=True)),
                ('bpm', models.IntegerField(blank=True, null=True)),
                ('divisions', models.IntegerField(blank=True, null=True)),
                ('tempo_text', models.CharField(blank=True, max_length=30)),
                ('views', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('ocassion', models.CharField(max_length=30)),
                ('genre', models.CharField(max_length=30)),
                ('youtube_playlist_id', models.CharField(blank=True, max_length=100, null=True)),
                ('drive_folder_id', models.CharField(blank=True, max_length=100, null=True)),
                ('authors', models.ManyToManyField(to='author.Author')),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Language')),
                ('likes', models.ManyToManyField(related_name='song_likes', to='siteuser.SiteUser')),
                ('mass_parts', models.ManyToManyField(to='song.MassPart')),
                ('seasons', models.ManyToManyField(to='song.Season')),
            ],
            options={
                'ordering': ('-like_count', 'title', '-created', 'publish', 'tempo_text'),
            },
        ),
        migrations.CreateModel(
            name='Voicing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='song',
            name='voicing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Voicing'),
        ),
    ]
