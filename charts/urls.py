from django.conf.urls import patterns, url, include
from django.views.generic.dates import *

from rest_framework import routers

from .views import *
from .feeds import LatestChartsFeeds

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'charts', ChartViewSet)

urlpatterns = patterns('',
                       # Date Based View
                       url(r'^charts/archive/$',
                           ChartArchiveIndexView.as_view(),
                           name="chart_archive_index"),
                       url(r'^charts/(?P<year>\d{4})/$',
                           ChartYearArchiveView.as_view(),
                           name="chart_archive_year"),
                       url(r'^charts/(?P<year>\d{4})/(?P<month>\d+)/$',
                           ChartMonthArchiveView.as_view(month_format='%m'),
                           name="chart_archive_month_numeric"),
                       url(r'^charts/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
                           ChartMonthArchiveView.as_view(),
                           name="chart_archive_month"),
                       url(r'^charts/(?P<year>\d{4})/week/(?P<week>\d+)/$',
                           ChartWeekArchiveView.as_view(),
                           name="chart_archive_week"),
                       url(r'^charts/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$',
                           ChartDayArchiveView.as_view(),
                           name="chart_archive_day"),
                       url(r'^charts/today/$',
                           ChartTodayArchiveView.as_view(),
                           name='chart_archive_today'),
                       # Generic Views
                       # Charts
                       url(r'^chart/(?P<pk>\d+)/$',
                           ChartDetailView.as_view(),
                           name='chart_detail'),
                       url(r'^charts/hindi/$',
                           ChartListView.as_view(language='HI'),
                           name='hindi_chart_list'),
                       url(r'^charts/english/$',
                           ChartListView.as_view(language='EN'),
                           name='english_chart_list'),
                       url(r'^charts/top-10-(?P<slug>[\w-]+)-songs/$',
                           CustomChartDetailView.as_view(),
                           name='custom_chart_detail'),
                       url(r'^charts/$',
                           ChartListView.as_view(),
                           name='chart_list'),
                       # Songs
                       url(r'^song/(?P<pk>\d+)/(?P<slug>[\w-]+)/$',
                           SongDetailView.as_view(),
                           name='song_detail'),
                       # url(r'^songs/english/$',
                       #    SongListView.as_view(language='EN'),
                       #    name='english_song_list'),
                       url(r'^songs/$',
                           SongListView.as_view(),
                           name='song_list'),
                       url(r'^$',
                           HomePageView.as_view(),
                           name='homepage'),
                       # Feeds
                       url(r'^latest/feeds/$',
                           LatestChartsFeeds(),
                           name='feeds'),
                       url(r'api/', include(router.urls), name="api")
                       )