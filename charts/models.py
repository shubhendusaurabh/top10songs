from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

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
        #return reverse('chart_detail', kwargs={'pk': self.pk})
        return ('chart_detail', [int(self.pk)])

    def __unicode__(self):
        return '%s' % (self.week)

    def scrap_songs_init(self):
        return mark_safe('<img class="loading" src="/static/img/loading.gif" alt="loading" style="display:none;" /><a class="task"><span class="glyphicon glyphicon-star"></span>Load</a>')
    scrap_songs_init.allow_tags = True
    scrap_songs_init.short_description = ('Scrap Songs')

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
