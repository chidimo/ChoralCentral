# Generated by Django 2.0.5 on 2018-06-02 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[('', 'Select an option'), ('anthem', 'Anthem'), ('carol', 'Carol'), ('chorus', 'Chorus'), ('folk music', 'Folk music'), ('gregorian chant', 'Gregorian Chant'), ('hymn', 'Hymn'), ('mass', 'Mass'), ('motet', 'Motet'), ('psalm', 'Psalm'), ('popular music', 'Popular music'), ('requiem', 'Requiem'), ('sequence', 'Sequence')], default='hymn', max_length=30),
        ),
    ]
