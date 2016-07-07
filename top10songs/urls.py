from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
# from rest_framework import routers, serializers, viewsets

from charts.sitemaps import ChartSitemap, SongSitemap, CustomChartSitemap
admin.autodiscover()

sitemaps = {
    'chart': ChartSitemap,
    'song': SongSitemap,
    'custom': CustomChartSitemap
}
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       url(r'^search/', include('search.urls')),
                       url(r'', include('charts.urls')),

                       )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
