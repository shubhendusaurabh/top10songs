from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from .models import Song, Chart

class ChartSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Chart.objects.all()

    def lastmod(self, obj):
        return obj.week
