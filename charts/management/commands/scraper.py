from urllib2 import urlopen
from urllib import urlencode
import datetime
import json
from django.core.exceptions import MultipleObjectsReturned
from bs4 import BeautifulSoup
from charts.models import Chart, Song, Ranking
from .billboard import fetchEntries

hindiURL = 'http://www.radiomirchi.com/more/mirchi-top-20/'
engURL = 'http://top10songs.com/'
YouTubeapi = 'https://www.googleapis.com/youtube/v3/search?'


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)


def init_chart(language):
    c = Chart()
    c.week = datetime.datetime.today()
    c.language = language
    c.save()
    return c


def get_youtube_id(songName):
    query_args = {'q': songName, 'part': 'id', 'key': 'AIzaSyATgfTV-ImD97mi2BWtIq19jmbSj8B_eR4'}
    encoded_args = urlencode(query_args)
    response = urlopen(YouTubeapi + encoded_args).read()
    parsed_response = json.loads(response)
    return parsed_response['items'][0]['id']['videoId']


def scrap_eng_songs():
    doc = make_soup(engURL)
    songs = doc.findAll("td", "left")
    c = init_chart("EN")
    for i in range(0, 20, 2):
        name = songs[i].text.strip()
        artist = songs[i+1].text.strip()
        try:
            s, created = Song.objects.get_or_create(name=name, artist=artist)
        except MultipleObjectsReturned:
            s = Song.objects.filter(name=name, artist=artist).first()
        if created:
            s.youtube_id = get_youtube_id(s.name)
            s.save()
        Ranking.objects.create(song=s, chart=c, position=(i/2)+1)


def scrap_eng_songs_new():
    songs = fetchEntries()
    c = init_chart('EN')
    i=1
    for song in songs:
        s, created = Song.objects.get_or_create(name=song.name, album=song.album, artist=song.artist)
        if created:
            s.youtube_id = get_youtube_id(s.name)
            s.save()
        Ranking.objects.create(song=s, chart=c, position=i)
        i+=1


def scrap_hindi_songs():
    doc = make_soup(hindiURL)
    songs = doc.findAll('div', 'header')
    c = init_chart("HI")
    ranking = Ranking()
    for i, song in enumerate(songs):
        if i < 10:
            name = song.contents[1].text.strip()
            album = song.contents[3].next.strip()
            artist = song.contents[3].next.next.next.strip()
            s, created = Song.objects.get_or_create(name=name, album=album, artist=artist)
            if created:
                s.youtube_id = get_youtube_id(s.name)
                s.save()
            Ranking.objects.create(song=s, chart=c, position=i+1)
