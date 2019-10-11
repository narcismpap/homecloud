from django.db import models
from django.contrib.auth.models import User

def cache_image_from_url(image_url):
    import os.path
    import requests
    from HomeCloud.settings import BASE_DIR

    import hashlib
    unique_key = hashlib.sha1(image_url).hexdigest()
    extension = str(image_url).split(".")[-1]

    destination_file = "/%s/cached_images/%s.%s" % ("media", unique_key, extension)

    if not os.path.isfile(BASE_DIR + destination_file):
        with open(BASE_DIR + destination_file, 'w+') as handle:
            response = requests.get( image_url, stream=True )

            if not response.ok:
                return None

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

            handle.close()

    return "/media/cached_images/%s.%s" % (unique_key, extension)


def translate_text_with_cache(text, to_language='ro'):
    return text

def translate_text_with_cache_legacy(text, to_language='ro'):
    import hashlib
    unique_key = hashlib.sha1(text).hexdigest()

    try:
        return TranslateCache.objects.get(key=unique_key, to_language=to_language).translated_string
    except TranslateCache.DoesNotExist:

        from libraries.translate import Translator
        translator= Translator(to_lang=to_language)
        translation = translator.translate(text)

        if translation:
            TranslateCache.objects.create(
                key = unique_key,
                original_string = text,
                translated_string = translation,
                to_language = to_language
            )

        return translation


class TranslateCache(models.Model):
    key = models.CharField(max_length=64, unique=True)
    original_string = models.TextField()
    translated_string = models.TextField()
    from_language = models.CharField(max_length=10, default="auto")
    to_language = models.CharField(max_length=10)

    def __str__(self):
        return "%s" % self.key


class Movie(models.Model):
    name = models.CharField(max_length=255)
    local_path = models.TextField()
    file_name = models.CharField(max_length=255)
    is_subtitled = models.BooleanField(default=False)
    first_addition = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    tmdb_id = models.IntegerField()
    imdb_id = models.CharField(max_length=32)
    overview = models.TextField()
    popularity = models.FloatField()
    release_date = models.DateField()
    revenue = models.FloatField(default=0)
    runtime = models.PositiveSmallIntegerField(default=0)
    tagline = models.CharField(max_length=255)
    vote_average = models.FloatField(default=0)
    poster_image = models.TextField()
    backdrop_image = models.TextField()
    youtube_video_code = models.CharField(max_length=255, default="")

    def get_formatted_runtime(self):
        import datetime
        return str(datetime.timedelta(minutes=self.runtime))

    def get_poster_url(self):
        if self.poster_image:
            image_cache = cache_image_from_url("http://image.tmdb.org/t/p/original/%s" % self.poster_image)

            if image_cache:
                return image_cache

        return "/static/avatar-empty.jpg"

    def get_poster_thumbnail_url(self):
        if self.poster_image:
            image_cache = cache_image_from_url("http://image.tmdb.org/t/p/w185/%s" % self.poster_image)

            if image_cache:
                return image_cache

        return "/static/avatar-empty.jpg"

    def get_linked_genres_count(self):
        return self.get_linked_genres(True)

    def get_linked_production_companies_count(self):
        return self.get_linked_production_companies(True)

    def get_linked_genres(self, count=False):
        rt = ""
        for g in self.get_genres():
            additional = (" (%d)" % MovieGenre.objects.filter(genre=g.genre).count() ) if count else ""
            rt += "<a href='/?filter=true&genre=%s&sb=false'>%s%s</a>, " % ( g.genre.pk, g.genre.name, additional )

        return rt[:-2] if rt else ""

    def get_linked_production_companies(self, count=False):
        rt = ""
        for g in self.get_production_companies():
            additional = (" (%d)" % MovieProductionCompany.objects.filter(production_company=g.production_company).count() ) if count else ""
            rt += "<a href='/?filter=true&companies=%s&sb=false'>%s%s</a>, " % ( g.production_company.pk, g.production_company.name, additional )

        return rt[:-2] if rt else ""

    def tagline_translated(self):
        try:
            import unidecode
            return translate_text_with_cache(unidecode.unidecode(self.tagline))
        except:
            return self.tagline

    def overview_translated(self):
        import unidecode
        return translate_text_with_cache(unidecode.unidecode(self.overview))

    def get_genres(self):
        return MovieGenre.objects.filter(movie=self)

    def get_production_companies(self):
        return MovieProductionCompany.objects.filter(movie=self)

    def get_cast(self):
        return Cast.objects.filter(movie=self).order_by("order")

    def __str__(self):
        return "%s" % self.name


class Cast(models.Model):
    name = models.CharField(max_length=255)
    cast_id = models.PositiveSmallIntegerField()
    actor = models.ForeignKey("Actor")
    movie = models.ForeignKey("Movie")
    credit = models.CharField(max_length=64)
    order = models.PositiveSmallIntegerField()
    profile_image = models.TextField()

    def __str__(self):
        from unidecode import unidecode
        return "%s played by %s" % ( unidecode(self.name), self.actor )


class Review(models.Model):
    author = models.CharField(max_length=255)
    tid = models.PositiveSmallIntegerField()
    content = models.TextField()
    url = models.TextField()
    movie = models.ForeignKey(Movie)

    def __str__(self):
        return "%s" % self.author


class ProductionCompany(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        from unidecode import unidecode
        return "%s" % unidecode(self.name)


class MovieProductionCompany(models.Model):
    movie = models.ForeignKey(Movie)
    production_company = models.ForeignKey(ProductionCompany)

    def __str__(self):
        return "%s %s" % (self.movie, self.production_company)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie)
    genre = models.ForeignKey(Genre)

    def __str__(self):
        return "%s %s" % (self.movie, self.genre)


class Actor(models.Model):
    name = models.CharField(max_length=255)
    birthday = models.DateField(default=None, null=True)
    tmdb_id = models.IntegerField()
    death = models.DateField(default=None, null=True)
    aliases = models.TextField()
    biography = models.TextField()
    place_of_birth = models.TextField()
    homepage = models.TextField()
    profile_image = models.TextField()

    def get_movies(self):
        movies = []
        for m in MovieActor.objects.filter(actor=self):
            movies.append(m.movie)

        return movies

    def list_aliases(self):
        import json
        return ", ".join( json.loads(self.aliases) ) if self.aliases != "{}" else None

    def calculate_age(self):
        from datetime import date

        if not self.birthday:
            return None

        today = date.today() if not self.death else self.death
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def get_age_range(self):
        return "%s - %s" % ( (self.birthday.year if self.birthday else "N/A"), (self.death.year if self.death else "N/A") )

    def get_biography_translated(self):
        if self.biography:
            import unidecode
            return translate_text_with_cache(unidecode.unidecode(self.biography))

        return ""

    def movie_appearances_count(self):
        return MovieActor.objects.filter(actor=self).count()


    def get_profile_image_original_url(self):
        if self.profile_image:
            return "http://image.tmdb.org/t/p/original/%s" % self.profile_image
            #image_cache = cache_image_from_url("http://image.tmdb.org/t/p/w185/%s" % self.profile_image)

            #if image_cache:
            #    return image_cache

        return "/static/avatar-empty.jpg"

    def get_profile_image_url(self):
        if self.profile_image:
            return "http://image.tmdb.org/t/p/w185/%s" % self.profile_image
            #image_cache = cache_image_from_url("http://image.tmdb.org/t/p/w185/%s" % self.profile_image)

            #if image_cache:
            #    return image_cache

        return "/static/avatar-empty.jpg"

    def __str__(self):
        from unidecode import unidecode
        return "%s" % unidecode(self.name)


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)

    def __str__(self):
        return "%s %s" % ( self.movie, self.actor )


class ViewedList(models.Model):
    movie = models.ForeignKey("Movie")
    user = models.ForeignKey(User)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s seen by %s" % (self.movie, self.user)


class PendingList(models.Model):
    movie = models.ForeignKey("Movie")
    user = models.ForeignKey(User)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s to be seen by %s" % (self.movie, self.user)
