# Generated by Django 2.0.5 on 2018-06-16 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='originator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser'),
        ),
        migrations.AlterField(
            model_name='request',
            name='originator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='siteuser.SiteUser'),
        ),
    ]