import re

from django.db import models
from django.core.urlresolvers import reverse

from django_extensions.db.models import AutoSlugField


class Chart(models.Model):
    LANGUAGES = (
        ('HI', 'Hindi'),
        ('EN', 'English'),
        ('PJ', 'Punjabi'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGES)
    songs = models.ManyToManyField('Song', through='Ranking')
    week = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_songs(self):
        return self.songs.order_by('song')

    class Meta:
        ordering = ['-week']

    def get_absolute_url(self):
        return reverse('chart_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return '%s' % (self.week)


class Song(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', null=True)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    youtube_id = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return '%s by %s' % (self.name, self.artist)

    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'pk': int(self.pk), 'slug': self.slug})

    def get_artists(self):
        if self.artist:
            return re.split(', |& |\Featuring\ ', self.artist)


class Ranking(models.Model):
    song = models.ForeignKey(Song, related_name='song')
    chart = models.ForeignKey(Chart)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('chart',)


class CustomChart(models.Model):
    about = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='about')
    songs = models.ManyToManyField('Song', through='CustomRanking')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_songs(self):
        return self.songs.order_by('customsong')

    def get_absolute_url(self):
        return reverse('custom_chart_detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return '%s' % (self.about)


class CustomRanking(models.Model):
    song = models.ForeignKey(Song, related_name='customsong')
    chart = models.ForeignKey(CustomChart)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('position',)

    def __unicode__(self):
        return '%s %s' % (self.position, self.song)
