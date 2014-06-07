from bs4 import BeautifulSoup
from urllib2 import urlopen

class ChartEntry:

    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album

    def __repr__(self):
        return '%s by %s ' % (self.name, self.artist)

def fetchEntries():
    songs = []
    url = 'http://www.billboard.com/charts/hot-100'
    soup = BeautifulSoup(urlopen(url).read())
    for entry_soup in soup.find_all('article', 'song_review'):
        name = entry_soup.header.h1.string.strip()
        chartInfoSoup = entry_soup.header.find('p', 'chart_info')
        if len(chartInfoSoup.contents) >= 4:
            # Both artist and album info
            artist = chartInfoSoup.contents[1].string
            album = chartInfoSoup.contents[4].string.strip()
        else:
            album = ''
            # only artist
            if chartInfoSoup.find('a'):
                artist = chartInfoSoup.find('a').string.strip()
            else:
                # Artist name not linked
                artist = chartInfoSoup.contents[0].string.strip()
        # self.entries.append(ChartEntry(title, artist, album))
        song = ChartEntry(name, artist, album)
        songs.append(song)
    return songs
