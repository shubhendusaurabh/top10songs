# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0002_song_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'about', editable=False, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField()),
                ('chart', models.ForeignKey(to='charts.CustomChart')),
                ('song', models.ForeignKey(related_name='customsong', to='charts.Song')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.AddField(
            model_name='customchart',
            name='songs',
            field=models.ManyToManyField(to='charts.Song', through='charts.CustomRanking'),
        ),
    ]
