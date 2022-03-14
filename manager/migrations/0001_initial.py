# Generated by Django 2.2 on 2022-03-11 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=120, unique=True)),
                ('current_version', models.TextField()),
                ('downloads', models.IntegerField()),
                ('views', models.IntegerField()),
                ('public', models.BooleanField()),
                ('tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_ID', models.CharField(max_length=20)),
                ('code', models.FileField(upload_to='packages/<package_name>')),
                ('dependencies', models.TextField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Package')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='avatars')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.UserProfile'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('posted_at', models.DateField()),
                ('likes', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.UserProfile')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Package')),
            ],
        ),
    ]