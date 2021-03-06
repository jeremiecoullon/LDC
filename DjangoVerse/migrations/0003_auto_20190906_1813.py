# Generated by Django 2.2.4 on 2019-09-06 18:13

import DjangoVerse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoVerse', '0002_festival_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=DjangoVerse.models.album_img_path),
        ),
        migrations.AddField(
            model_name='band',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=DjangoVerse.models.band_img_path),
        ),
        migrations.AddField(
            model_name='player',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=DjangoVerse.models.player_img_path),
        ),
        migrations.AddField(
            model_name='venue',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=DjangoVerse.models.venue_img_path),
        ),
    ]
