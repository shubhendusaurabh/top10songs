from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',

        url(
            regex   = '^$',
            view    = 'search',
            name    = 'search'
        ),

        url(
            regex   = '^/autocomplete/$',
            view    = 'search_autocomplete',
            name    = 'search_autocomplete'
        ),
)
