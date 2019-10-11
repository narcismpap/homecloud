from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse

from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from ui.movies import MovieHelper
from ui.actor import ActorHelper
import home.models as HM


def auto_login(request):
    if "lockdown-allow" not in request.session:
        from HomeCloud.settings import LOCKDOWN_PASSWORDS
        request.session["lockdown-allow"] = LOCKDOWN_PASSWORDS[0]

        return redirect(request.path)

    return home(request)


def search(request):
    import json, urllib2
    results = []

    if request.method == "POST":
        data = json.load( urllib2.urlopen(request.POST["source"]) )
        results = data["MovieList"]

    variables = { "results": results, "Title": _("Cautare Filme"), "SourceLink": request.POST["source"] if "source" in request.POST else None, "CurrentUser": request.user }
    return render_to_response("pages/search.html", variables, context_instance=RequestContext(request))


def home(request):
    ui = MovieHelper(request)
    return ui.page_all()


def movies_by_category(request, category_id):
    ui = MovieHelper(request)
    return ui.page_filter_by_genre( HM.Genre.objects.get(pk=category_id) )


def movies_by_actor(request, actor_id):
    ui = MovieHelper(request)
    return ui.page_filter_by_actor( HM.Actor.objects.get(pk=actor_id) )


def actor_details(request, actor_id):
    ui = ActorHelper(request)
    return ui.page_actor_details( HM.Actor.objects.get(pk=actor_id) )


def movie_details(request, movie_id):
    ui = MovieHelper(request)
    return ui.page_movie_details( HM.Movie.objects.get(pk=movie_id) )


def image(request, image_id):
    import os.path
    import requests
    from HomeCloud.settings import MEDIA_ROOT

    destination_file = "%scached_images/%s" % (MEDIA_ROOT, image_id)

    if not os.path.isfile(destination_file):
        with open(destination_file, 'wb') as handle:
            response = requests.get( "http://image.tmdb.org/t/p/original/%s" % image_id, stream=True )

            if not response.ok:
                raise Http404

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

            handle.close()

    from django.views.static import serve
    return serve(request, os.path.basename(destination_file), os.path.dirname(destination_file))


def view_login(request):
    from django.core.context_processors import csrf
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.models import User

    if request.method == "POST":
        for u in User.objects.filter(is_staff=False):
            if "selected_user_%d" % u.pk in request.POST:
                user = authenticate(username=u.username, password=u.username)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("/")

    variables = { "Title": _("Autentificare"), "AvailableSimpleUsers": User.objects.filter(is_staff=False) }
    return render_to_response("pages/login.html", variables, context_instance=RequestContext(request))


@login_required
def view_logout(request):
    from django.contrib import auth
    auth.logout(request)
    return redirect("/")


@login_required
def add_to_seen_list(request, movie_id):
    movie = HM.Movie.objects.get(pk=movie_id)
    if HM.ViewedList.objects.filter(user=request.user, movie=movie).count() == 0:
        HM.ViewedList.objects.create(user=request.user, movie=movie)

        try:
            HM.PendingList.objects.get(user=request.user, movie=movie).delete()
        except HM.PendingList.DoesNotExist:
            pass

    import json
    return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")


@login_required
def add_to_view_list(request, movie_id):
    movie = HM.Movie.objects.get(pk=movie_id)
    if HM.PendingList.objects.filter(user=request.user, movie=movie).count() == 0:
        HM.PendingList.objects.create(user=request.user, movie=movie)

    import json
    return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")


@login_required
def list_viewed(request):
    movies = []
    for m in HM.ViewedList.objects.filter(user=request.user):
        movies.append(m.movie)

    variables = { "Title": _("Filme Vizionate"), "ViewedListMovies": movies, "CurrentUser": request.user, "CanRemove": True }
    return render_to_response("pages/list_viewed_movies.html", variables, context_instance=RequestContext(request))


@login_required
def list_pending(request):
    movies = []
    for m in HM.PendingList.objects.filter(user=request.user):
        movies.append(m.movie)

    variables = { "Title": _("Lista de Vizionare"), "PendingListMovies": movies, "CurrentUser": request.user, "CanRemove": True }
    return render_to_response("pages/list_pending_movies.html", variables, context_instance=RequestContext(request))


@login_required
def remove_list(request, movie_id):
    movie = HM.Movie.objects.get(pk=movie_id)

    try:
        HM.PendingList.objects.get(user=request.user, movie=movie).delete()
    except HM.PendingList.DoesNotExist:
        pass

    try:
        HM.ViewedList.objects.get(user=request.user, movie=movie).delete()
    except HM.ViewedList.DoesNotExist:
        pass

    import json
    return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")