# Generated by Django 2.0.5 on 2018-05-16 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='siteuser.SiteUser'),
        ),
    ]
