from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Caches all the movie images available in the system for faster reloading at a later point'

    def handle(self, *args, **options):
        from home.models import Movie
        import time

        for m in Movie.objects.all():
            print "Loading assets for %s" % m.name
            m.get_poster_thumbnail_url()
            m.get_poster_url()
            #time.sleep(1)

        self.stdout.write("Loaded all assets")