from django.contrib.sitemaps import Sitemap
from .models import Chart, Song


class ChartSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Chart.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class SongSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Song.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
