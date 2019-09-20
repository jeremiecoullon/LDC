# Generated by Django 2.2.4 on 2019-09-20 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoVerse', '0005_auto_20190911_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='video_embed',
            field=models.CharField(blank=True, default='', help_text='Paste the URL to the youtube video', max_length=300, verbose_name='Youtube URL'),
        ),
    ]
