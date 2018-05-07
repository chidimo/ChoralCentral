# Generated by Django 2.0.1 on 2018-05-07 11:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0001_initial'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('language', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MassPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('part', models.CharField(choices=[('', 'Select Mass part'), ('ENTRANCE', 'Entrance'), ('KYRIE', 'Kyrie'), ('GLORIA', 'Gloria'), ('ACCLAMATION', 'Acclamation'), ('OFFERTORY', 'Offertory'), ('COMMUNION', 'Communion'), ('SANCTUS', 'Sanctus'), ('AGNUS DEI', 'Agnus Dei'), ('RECESSION', 'Recesssion'), ('CAROL', 'Carol'), ('GENERAL', 'General'), ('NA', 'NA')], max_length=15, unique=True)),
                ('about', models.TextField()),
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
                ('season', models.CharField(choices=[('', 'Select Season'), ('ORDINARY TIME', 'Ordinary Time'), ('ADVENT', 'Advent'), ('CHRISTMAS', 'Christmas'), ('LENT', 'Lent'), ('EASTER', 'Easter'), ('PENTECOST', 'Pentecost'), ('NA', 'NA')], max_length=15, unique=True)),
                ('about', models.TextField()),
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
                ('compose_date', models.DateField(blank=True, null=True)),
                ('slug', universal.fields.AutoSlugField(blank=True, editable=False, max_length=255, set_once=True, set_using='title')),
                ('lyrics', models.TextField(blank=True)),
                ('first_line', models.CharField(blank=True, max_length=100)),
                ('scripture_reference', models.CharField(blank=True, max_length=25)),
                ('tempo', models.IntegerField(blank=True, null=True)),
                ('tempo_text', models.CharField(blank=True, max_length=30)),
                ('bpm', models.IntegerField(blank=True, null=True)),
                ('divisions', models.IntegerField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('youtube_playlist_id', models.CharField(blank=True, max_length=100, null=True)),
                ('drive_folder_id', models.CharField(blank=True, max_length=100, null=True)),
                ('authors', models.ManyToManyField(to='author.Author')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Language')),
                ('likes', models.ManyToManyField(related_name='song_likes', to='siteuser.SiteUser')),
                ('mass_parts', models.ManyToManyField(to='song.MassPart')),
                ('originator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
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
                ('voicing', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='song',
            name='voicing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Voicing'),
        ),
    ]
