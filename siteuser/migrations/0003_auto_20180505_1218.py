# Generated by Django 2.0.1 on 2018-05-05 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0002_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='siteuser',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siteuser.SiteUser'),
        ),
    ]
