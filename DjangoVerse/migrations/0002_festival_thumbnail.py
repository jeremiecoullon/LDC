# Generated by Django 2.2.4 on 2019-09-06 18:10

import DjangoVerse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoVerse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='festival',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=DjangoVerse.models.festival_img_path),
        ),
    ]