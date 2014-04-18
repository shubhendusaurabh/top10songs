from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Chart(models.Model):
    LANGUAGES = (
        ('HI', 'Hindi'),
        ('EN', 'English'),
        ('PJ', 'Punjabi'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGES)
    week = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-week']
    @models.permalink
    def get_absolute_url(self):
        return reverse('chart_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return '%s' % (self.week)

class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    youtube_id = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    chart = models.ForeignKey(Chart)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return '%s by %s' % (self.name, self.artist)

    @models.permalink
    def get_absolute_url(self):
        return ('song_detail', [int(self.pk)])
