from django.contrib.syndication.views import Feed
from .models import Chart

class LatestChartsFeeds(Feed):
    title = 'Top 10 Songs'
    link = '/charts/'
    description = "Top 10 Songs in English, Hindi. Weekly Updated"

    def items(self):
        return Chart.objects.order_by('-week')[:10]

    def item_title(self, item):
        return "Top 10 " + item.get_language_display() + " Songs in " + item.week.strftime("%B %d, %Y")

    def item_description(self, item):
        songs = item.song_set.all()
        content = '<ul>'
        template = '<li><a href="%s">%s</a></li>'
        for song in songs:
            temp = template % (song.get_absolute_url(),song.name)
            content += temp
        return content + '</ul>'
