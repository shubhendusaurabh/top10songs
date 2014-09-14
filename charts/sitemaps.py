from django.contrib.sitemaps import Sitemap
from .models import Chart


class ChartSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Chart.objects.all()

    def lastmod(self, obj):
        return obj.week
