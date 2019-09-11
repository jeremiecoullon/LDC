# Generated by Django 2.2.4 on 2019-09-11 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_gig'),
    ]

    operations = [
        migrations.AddField(
            model_name='volume',
            name='pre_order',
            field=models.CharField(blank=True, help_text='Add link to pre-order page', max_length=500),
        ),
        migrations.AddField(
            model_name='volume',
            name='release_date',
            field=models.CharField(blank=True, help_text="Type in the release date that will appear on the homepage if the volume is in 'draft'", max_length=200),
        ),
    ]