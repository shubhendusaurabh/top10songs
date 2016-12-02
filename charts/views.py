from datetime import date
from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.db.models import Count
from rest_framework import viewsets

from .models import Chart, Song, CustomChart, Ranking
from .serializers import SongSerializer, ChartSerializer

import logging

logger = logging.getLogger(__name__)

class ChartArchiveIndexView(ArchiveIndexView):
    model = Chart
    date_field = 'week'

    def get_context_data(self, **kwargs):
        context = super(ChartArchiveIndexView, self).get_context_data(**kwargs)
        charts = Chart.objects.all()
        archive = {}

        years = charts.dates(self.date_field, 'year')[::-1]
        for date_year in years:
            month = charts.filter(week__year=date_year.year).dates(
                self.date_field, 'month')
            archive[date_year] = month

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive
        context['top_songs'] = Ranking.objects.annotate(num_week=Count('song')).order_by('-num_week')[:10]
        return context


class ChartYearArchiveView(YearArchiveView):
    model = Chart
    paginate_by = 20
    date_field = 'week'
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(ChartYearArchiveView, self).get_context_data(**kwargs)
        year = kwargs.get('date_list')
        year = year[0].year
        context['top_songs'] = Ranking.objects.filter(chart__week__year=year).annotate(num_week=Count('song')).order_by('-num_week')[:10]
        return context


class ChartMonthArchiveView(MonthArchiveView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(ChartMonthArchiveView, self).get_context_data(**kwargs)
        chart_date = kwargs.get('date_list')
        chart_start_date = chart_date[0]
        chart_end_date = chart_date[len(chart_date) - 1]
        # chart_end_date = date.today()
        context['top_songs'] = Ranking.objects.filter(chart__week__range=(chart_start_date, chart_end_date)).annotate(num_week=Count('song')).order_by('-num_week')[:10]
        return context


class ChartWeekArchiveView(WeekArchiveView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    week_format = "%W"
    allow_future = True


class ChartDayArchiveView(DayArchiveView):
    queryset = Chart.objects.all()
    date_field = "week"
    month_format = "%m"
    make_object_list = True
    allow_future = True


class ChartTodayArchiveView(TodayArchiveView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    allow_future = True


class ChartDateDetailView(DateDetailView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    allow_future = True


class ChartDetailView(DetailView):
    queryset = Chart.objects.prefetch_related('songs')


class SongDetailView(DetailView):
    queryset = Song.objects.select_related()


class ChartListView(ListView):
    language = ""
    model = Chart
    paginate_by = 20

    # def get_queryset(self, **kwargs):
        # queryset = super(ChartListView, self).get_queryset(**kwargs)
        # if self.language:
            # logger.error(self.language)
            # queryset.filter(language=self.language)
        # else:
            # logger.error('no lang')
        # return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ChartListView, self).get_context_data(**kwargs)
        if self.language:
            context['chart_list'] = Chart.objects.filter(language=self.language)
            context['language'] = dict(Chart.LANGUAGES)[self.language]
        # else:
            # context['charts'] = Chart.objects.all()
        return context


class SongListView(ListView):
    model = Song
    paginate_by = 20
    queryset = Song.objects.order_by('name')


class HomePageView(TemplateView):
    template_name = 'charts/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_charts'] = Chart.objects.all()[:2]
        return context

class CustomChartDetailView(DetailView):
    queryset = CustomChart.objects.prefetch_related('songs')

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.order_by('name')
    serializer_class = SongSerializer

class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer