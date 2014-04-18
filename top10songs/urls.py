from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from charts.models import Chart, Song
from charts.sitemaps import ChartSitemap
admin.autodiscover()

info_dict  = {
    'queryset': Chart.objects.all(),
    'date_field': 'week',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    #'chart': GenericSitemap(info_dict, priority=0.6),
    #'charts': ChartSitemap,
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'top10songs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^page/', include('django.contrib.flatpages.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'', include('charts.urls')),

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )
