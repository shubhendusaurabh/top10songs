from django.core.management.base import BaseCommand, CommandError
import scraper

class Command(BaseCommand):
    args = '<url url ...>'
    help = 'Scraps the data from the url'

    def handle(self, *args, **options):
        try:
            #scraper.scrap_hindi_songs()
            scraper.scrap_eng_songs_new()
        except:
            raise CommandError('Oh Shoot')

        self.stdout.write('Successfully fetched data')
