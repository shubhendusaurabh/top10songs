#!/usr/bin/env python
#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "top10songs.settings")
from urllib2 import urlopen
from urllib import urlencode
import datetime
import json
from bs4 import BeautifulSoup
from charts.models import Chart,Song

hindiURL = 'http://www.radiomirchi.com/more/mirchi-top-20/'
engURL = 'http://top10songs.com/'
YouTubeapi = 'http://gdata.youtube.com/feeds/api/videos/?v=2&alt=jsonc&paid-content=false&max-results=1&'

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
    query_args = { 'q': songName }
    encoded_args = urlencode(query_args)
    response = urlopen(YouTubeapi+encoded_args).read()
    parsed_response = json.loads(response)
    return parsed_response['data']['items'][0]['id']

def scrap_eng_songs():
    doc = make_soup(engURL)
    songs = doc.findAll("td", "left")
    c = init_chart("EN")
    for i in range(0,20,2):
        s = Song()
        s.name = songs[i].text.strip()
        s.artist = songs[i+1].text.strip()
        s.youtube_id = get_youtube_id(s.name)
        s.chart = c
        s.save()

def scrap_hindi_songs():
    doc = make_soup(hindiURL)
    songs = doc.findAll('div', 'header')
    c = init_chart("HI")
    for i,song in enumerate(songs):
        if i < 10:
            s = Song()
            s.name = song.contents[1].text.strip()
            s.album = song.contents[3].next.strip()
            s.publisher = song.contents[3].next.next.next.strip()
            s.youtube_id = get_youtube_id(s.name)
            s.chart = c
            s.save()

#if __name__ == '__main__':
#    scrap_hindi_songs()
