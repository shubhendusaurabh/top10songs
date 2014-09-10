from datetime import date
from django.shortcuts import render
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from .models import Chart, Song


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
        return context


class ChartYearArchiveView(YearArchiveView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    allow_future = True


class ChartMonthArchiveView(MonthArchiveView):
    queryset = Chart.objects.all()
    date_field = 'week'
    make_object_list = True
    allow_future = True


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

    def get_queryset(self):
        if self.language:
            return Chart.objects.filter(language=self.language)
        else:
            return Chart.objects.all()


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
