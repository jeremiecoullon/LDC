# Generated by Django 2.2.3 on 2019-08-03 08:50

import ckeditor.fields
from django.db import migrations, models
import music.util


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=music.util.player_image_directory_path)),
                ('bio', ckeditor.fields.RichTextField(default='player bio')),
            ],
        ),
        migrations.CreateModel(
            name='Tune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=music.util.tune_image_directory_path)),
                ('video_embed', models.CharField(blank=True, default='', max_length=300, verbose_name='Youtube URL')),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
    ]
