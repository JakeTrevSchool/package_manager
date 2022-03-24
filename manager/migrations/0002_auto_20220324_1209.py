# Generated by Django 2.2.26 on 2022-03-24 12:09

from django.db import migrations, models
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='readme',
        ),
        migrations.AddField(
            model_name='package',
            name='readme',
            field=models.FileField(null=True, upload_to=manager.models.Package.getUploadDir),
        ),
    ]
