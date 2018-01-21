# Generated by Django 2.0.1 on 2018-01-21 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields
import utils


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
                ('file', models.FileField(upload_to=utils.upload_midi)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to=utils.upload_pdf)),
                ('likes', models.ManyToManyField(related_name='score_likes', to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('-created',),
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
                ('video_link', models.URLField(max_length=250, unique=True)),
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
            field=models.ManyToManyField(to='song_media.ScoreNotation'),
        ),
        migrations.AddField(
            model_name='score',
            name='part',
            field=models.ManyToManyField(to='song_media.VocalPart'),
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
            field=models.ManyToManyField(to='song_media.VocalPart'),
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
