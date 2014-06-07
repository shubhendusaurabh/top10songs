from django.contrib import admin
from django.http import Http404, HttpResponse
from django.conf.urls import patterns
from .models import *
from django.core.management import call_command

class ChartAdmin(admin.ModelAdmin):
    class Media:
        js = (
                '/static/js/admin_tasks.js',
            )

    def get_urls(self):
        urls = super(ChartAdmin, self).get_urls()
        extra_urls = patterns('',
                (r'^scrap-songs/$', self.admin_site.admin_view(self.task_view))
        )
        return extra_urls + urls

    def task_view(self, request):
        from StringIO import StringIO
        content = StringIO()
        result = call_command('runscraper', use_natural_keys=True, stdout=content)
        content.seek(0)
        # TODO:: design the template for the view
        return HttpResponse(content.read())

admin.site.register(Chart, ChartAdmin)
admin.site.register(Song)
