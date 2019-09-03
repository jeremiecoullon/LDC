# Generated by Django 2.2.4 on 2019-09-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_volume_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('gig_link', models.CharField(blank=True, max_length=200)),
                ('gig_date', models.DateTimeField(verbose_name='Gig date')),
                ('preview_date_admin', models.CharField(blank=True, help_text='This will override the date above when shown on the site. Otherwise leave blank', max_length=200, null=True, verbose_name='date')),
            ],
        ),
    ]
