# Generated by Django 2.0.5 on 2018-05-27 08:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sorl.thumbnail.fields
import universal.fields
from .. import utils

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0001_initial'),
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Midi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fformat', models.CharField(blank=True, max_length=10)),
                ('fsize', models.FloatField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('media_file', models.FileField(blank=True, null=True, upload_to=utils.save_midi)),
                ('downloads', models.IntegerField(default=0)),
                ('drive_view_link', models.URLField(blank=True, null=True)),
                ('drive_download_link', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-downloads', 'created'),
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fsize', models.FloatField(blank=True, null=True)),
                ('media_file', models.FileField(null=True, upload_to=utils.save_score)),
                ('thumbnail', models.ImageField(null=True, upload_to=utils.save_score_thumbnail)),
                ('downloads', models.IntegerField(default=0)),
                ('drive_view_link', models.URLField(blank=True, null=True)),
                ('drive_download_link', models.URLField(blank=True, null=True)),
                ('embed_link', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-downloads', 'created'),
            },
        ),
        migrations.CreateModel(
            name='ScoreNotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default='Solfa', max_length=30, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('video_link', models.URLField(max_length=100, unique=True)),
                ('channel_link', models.URLField(default='', max_length=100)),
                ('playlist', models.CharField(default='playlist', max_length=100)),
                ('video_playlist_link', models.CharField(default='playlist link', max_length=100)),
                ('title', models.CharField(default='video title', max_length=100)),
                ('youtube_likes', models.IntegerField(default=0)),
                ('youtube_views', models.IntegerField(default=0)),
                ('thumbnail', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=utils.save_video_thumbnail)),
                ('thumbnail_url', models.URLField(default='www.youtube.com')),
                ('song', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='VocalPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default='Choir', max_length=30, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='score',
            name='notation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song_media.ScoreNotation'),
        ),
        migrations.AddField(
            model_name='score',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song_media.VocalPart'),
        ),
        migrations.AddField(
            model_name='score',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Song'),
        ),
        migrations.AddField(
            model_name='score',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='siteuser.SiteUser'),
        ),
        migrations.AddField(
            model_name='midi',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song_media.VocalPart'),
        ),
        migrations.AddField(
            model_name='midi',
            name='song',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song'),
        ),
        migrations.AddField(
            model_name='midi',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='siteuser.SiteUser'),
        ),
    ]
