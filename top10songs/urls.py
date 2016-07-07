from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
# from rest_framework import routers, serializers, viewsets

from charts.sitemaps import ChartSitemap, SongSitemap, CustomChartSitemap
admin.autodiscover()

def acme(request, acme_token):
    import os
    from django.http import HttpResponse, Http404
    acme_key = ''
    if ('ACME_KEY' in os.environ and 'ACME_TOKEN' in os.environ):
        if acme_token == os.environ['ACME_TOKEN']:
            acme_key = os.environ['ACME_KEY']

    for key in os.environ:
        if key.startswith('ACME_TOKEN_'):
            num = key.split('ACME_TOKEN_')[1]
            if acme_token == os.environ['ACME_TOKEN_' + num]:
                acme_key = os.environ['ACME_KEY_' + num]
    if acme_key:
        return HttpResponse(acme_key)
    else:
        raise Http404

sitemaps = {
    'chart': ChartSitemap,
    'song': SongSitemap,
    'custom': CustomChartSitemap
}
urlpatterns = patterns('',
                       url(r'^.well-known/acme-challenge/(?P<acme_token>[\w\-]+)$', acme, name='acme-challenge'),
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
