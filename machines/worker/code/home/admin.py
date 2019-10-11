from django.contrib import admin
from home.models import Movie, Actor, MovieProductionCompany, MovieGenre, MovieActor, Cast, Review

class CastInline(admin.StackedInline):
    model = Cast

class MovieProductionCompanyInline(admin.StackedInline):
    model = MovieProductionCompany

class MovieGenreInline(admin.StackedInline):
    model = MovieGenre

class MovieActoriInline(admin.StackedInline):
    model = MovieActor

class ReviewInline(admin.StackedInline):
    model = Review


class MovieAdmin(admin.ModelAdmin):
    #inlines = [ CastInline, MovieProductionCompanyInline, MovieGenreInline, MovieActoriInline, ReviewInline ]
    inlines = [ MovieProductionCompanyInline, MovieGenreInline, ReviewInline ]
    list_display = ('name', 'tmdb_id', 'runtime', 'first_addition' )

admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)