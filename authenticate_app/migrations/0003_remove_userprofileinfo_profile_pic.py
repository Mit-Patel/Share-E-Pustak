# Generated by Django 3.0.3 on 2020-02-27 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate_app', '0002_auto_20200225_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='profile_pic',
        ),
    ]