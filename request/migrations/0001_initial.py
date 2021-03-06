# Generated by Django 2.0.6 on 2018-07-01 01:23

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
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('request',),
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('answer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song')),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser')),
            ],
            options={
                'ordering': ('status', '-created'),
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Request'),
        ),
        migrations.AddField(
            model_name='reply',
            name='song',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='song.Song'),
        ),
    ]
