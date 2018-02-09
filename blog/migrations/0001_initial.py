# Generated by Django 2.0.1 on 2018-02-09 20:12

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '__first__'),
        ('song', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('comment', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to='siteuser.SiteUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published')], default='DRAFT', max_length=12)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('slug', universal.fields.AutoSlugField(blank=True, editable=False, set_once=True, set_using='title')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
                ('song', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='song.Song')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('published_set', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
