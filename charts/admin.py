from django.contrib import admin
from .models import *

class SongInline(admin.StackedInline):
    model = Chart.songs.through
    extra = 10

class ChartAdmin(admin.ModelAdmin):
    inlines = [SongInline]

class CustomSongInline(admin.StackedInline):
    model = CustomChart.songs.through
    extra = 10

class CustomChartAdmin(admin.ModelAdmin):
    inlines = [CustomSongInline]

admin.site.register(Chart, ChartAdmin)
admin.site.register(Song)
admin.site.register(CustomChart, CustomChartAdmin)
admin.site.register(CustomRanking)
