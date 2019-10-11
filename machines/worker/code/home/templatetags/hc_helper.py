from django import template
import home.models as HM

register = template.Library()


@register.filter(name='is_movie_added_to_pending')
def is_movie_added_to_pending(movie, user):
    if user and movie:
        return HM.PendingList.objects.filter(user=user, movie=movie).count() > 0
    return False

@register.filter(name='is_movie_added_to_seen')
def is_movie_added_to_seen(movie, user):
    if user and movie:
        return HM.ViewedList.objects.filter(user=user, movie=movie).count() > 0
    return False


@register.filter(name='has_movie_by_imdb')
def has_movie_by_imdb(imdb_code):
    try:
        if HM.Movie.objects.get(imdb_id=imdb_code):
            return "YES"
    except HM.Movie.DoesNotExist:
        return "NO"