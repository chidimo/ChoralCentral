# Generated by Django 2.0.5 on 2018-05-27 08:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('bio', models.TextField(blank=True, null=True)),
                ('slug', universal.fields.AutoMultipleSlugField(blank=True, editable=False, max_length=255, set_once=True, set_using=['last_name', 'first_name'])),
                ('author_type', models.CharField(choices=[('', 'Select author type'), ('LYRICIST', 'Lyricist'), ('COMPOSER', 'Composer')], default='COMPOSER', max_length=15)),
                ('likes', models.ManyToManyField(related_name='author_likes', to='siteuser.SiteUser')),
                ('originator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
    ]
