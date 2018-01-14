# Generated by Django 2.0 on 2017-12-29 20:45

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
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('language', models.CharField(max_length=25, unique=True)),
                ('originator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
