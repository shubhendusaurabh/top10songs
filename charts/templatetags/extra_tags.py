from django import template
from django.contrib.flatpages.models import FlatPage

from charts.models import CustomChart

register = template.Library()

@register.inclusion_tag("footer.html")
def footer_links():
    flatpages = FlatPage.objects.all()
    return { 'flatpages': flatpages }

@register.inclusion_tag("header.html")
def header_links():
    custom_charts = CustomChart.objects.all()
    return { 'custom_charts': custom_charts }
