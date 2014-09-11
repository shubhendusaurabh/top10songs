# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=2, choices=[(b'HI', b'Hindi'), (b'EN', b'English'), (b'PJ', b'Punjabi')])),
                ('week', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-week'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField()),
                ('chart', models.ForeignKey(to='charts.Chart')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255, blank=True)),
                ('album', models.CharField(max_length=255, blank=True)),
                ('youtube_id', models.CharField(max_length=255, blank=True)),
                ('publisher', models.CharField(max_length=255, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ranking',
            name='song',
            field=models.ForeignKey(related_name=b'song', to='charts.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='songs',
            field=models.ManyToManyField(to='charts.Song', through='charts.Ranking'),
            preserve_default=True,
        ),
    ]
