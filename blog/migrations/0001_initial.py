# Generated by Django 2.0.6 on 2018-07-01 01:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0001_initial'),
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('like_count', models.IntegerField(default=0)),
                ('comment', models.TextField()),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
                ('likes', models.ManyToManyField(related_name='comment_likes', to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('-like_count', 'created'),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100, null=True)),
                ('body', models.TextField()),
                ('slug', universal.fields.AutoSlugField(blank=True, editable=False, set_once=False, set_using='title')),
                ('publish', models.BooleanField(default=False)),
                ('like_count', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
                ('likes', models.ManyToManyField(related_name='post_likes', to='siteuser.SiteUser')),
                ('song', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song')),
            ],
            options={
                'ordering': ('-like_count', '-created', 'title'),
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
