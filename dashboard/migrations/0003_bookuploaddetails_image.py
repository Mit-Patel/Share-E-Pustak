# Generated by Django 3.0.3 on 2020-02-27 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200228_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookuploaddetails',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/'),
        ),
    ]