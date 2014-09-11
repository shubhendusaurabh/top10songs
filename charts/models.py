from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

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

    @models.permalink
    def get_absolute_url(self):
        # return reverse('chart_detail', kwargs={'pk': self.pk})
        return ('chart_detail', [int(self.pk)])

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

    @models.permalink
    def get_absolute_url(self):
        return ('song_detail', [int(self.pk)])


class Ranking(models.Model):
    song = models.ForeignKey(Song, related_name='song')
    chart = models.ForeignKey(Chart)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('position',)
