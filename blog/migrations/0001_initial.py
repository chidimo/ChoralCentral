# Generated by Django 2.0.1 on 2018-03-28 10:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('song', '0001_initial'),
        ('siteuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('like_count', models.IntegerField(default=1)),
                ('comment', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to='siteuser.SiteUser')),
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
                ('slug', universal.fields.AutoSlugField(blank=True, editable=False, set_once=True, set_using='title')),
                ('publish', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=1)),
                ('like_count', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to='siteuser.SiteUser')),
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
