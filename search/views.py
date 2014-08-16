import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

from .forms import SearchForm
from charts.models import Song


def search_function(q):
    # todo return all if empty q and check company
    items = []
    if q:
        items = Song.objects.select_related().filter(
                Q(name__icontains=q) |
                Q(artist__startswith=q.lower()) |
                Q(album__icontains=q) )
    else:
        items = Song.objects.select_related()
    return items

def search(request):

    q = request.GET.get('q', '')
    template_name = 'search/search.html'

    if '/' in q:
        lst = q.split('/')
        try:
            if lst[-1]:
                q = lst[-1]
            else:
                q = lst[-2]
        except IndexError:
            pass

    try:
        song = Song.objects.get(name__icontains=q)
        url = song.get_absolute_url()
        return HttpResponseRedirect(url)
    except Song.DoesNotExist:
        pass
    except Song.MultipleObjectsReturned:
        pass

    form = SearchForm(request.GET or None)

    return render(request, template_name, { 'songs': search_function(q), 'form': form })


def search_autocomplete(request):
    q = request.GET.get('term', '')
    if q:
        objects = search_function(q)[:15]
        objects = objects.values_list('title', flat=True)
        json_response = json.dumps(list(objects))
    else:
        json_response = json.dumps([])

    return HttpResponse(json_response, mimetype='text/javascript')
