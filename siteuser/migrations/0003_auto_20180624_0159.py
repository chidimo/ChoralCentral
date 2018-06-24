# Generated by Django 2.0.5 on 2018-06-23 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0002_auto_20180618_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='siteuser',
        ),
        migrations.RemoveField(
            model_name='groupjoinrequest',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='groupjoinrequest',
            name='group_of_interest',
        ),
        migrations.RemoveField(
            model_name='groupmembership',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='groupmembership',
            name='group',
        ),
        migrations.RemoveField(
            model_name='siteusergroup',
            name='members',
        ),
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.DeleteModel(
            name='GroupJoinRequest',
        ),
        migrations.DeleteModel(
            name='GroupMembership',
        ),
        migrations.DeleteModel(
            name='SiteUserGroup',
        ),
    ]