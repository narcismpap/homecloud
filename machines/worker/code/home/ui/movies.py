from collections import OrderedDict
from django.utils.translation import ugettext as _
import base
import home.models as HM

RESULTS_PER_PAGE = 24


class MovieFilterHelper:

    def __init__(self):
        pass

    def get_available_genre(self):
        categories = OrderedDict()
        for c in HM.Genre.objects.all().order_by("name"):
            categories[ str(c.pk) ] = c.name

        return categories

    def get_available_years(self):
        years = {}
        for m in HM.Movie.objects.all():
            if m.release_date and m.release_date.strftime("%Y") not in years:
                years[ m.release_date.strftime("%Y")] = True

        data = years.keys()
        data.sort(reverse=True)
        return data

    def get_production_companies(self):
        pcompany = OrderedDict()
        for c in HM.ProductionCompany.objects.all().order_by("name"):
            pcompany[ str(c.pk) ] = c.name

        return pcompany


class MovieHelper(base.BaseUI):

    def __init__(self, request):
        base.BaseUI.__init__(self, request)
        self.is_filter = False
        self.filter_genre = None
        self.filter_years = None
        self.filter_company = None
        self.keyword = None
        self.only_subtitled = None
        self.filter_order = "standard"
        self.current_pagination = 1
        self.only_unlisted = False

        if "filter" in self.request.GET:
            self.is_filter = True
            self.filter_genre = ( str(self.request.GET["genre"]).split(",") if "genre" in self.request.GET else [] )
            self.filter_years = ( str(self.request.GET["years"]).split(",") if "years" in self.request.GET else [] )
            self.filter_company = ( str(self.request.GET["companies"]).split(",") if "companies" in self.request.GET else [] )
            self.keyword = ( str(self.request.GET["keyword"]) if "keyword" in self.request.GET else None )
            self.only_subtitled = ( bool(self.request.GET["sb"] == "true") if "sb" in self.request.GET else False )
            self.filter_order = ( self.request.GET["order"] if "order" in self.request.GET else "standard" )
            self.only_unlisted = ( bool(self.request.GET["ou"] == "true") if "ou" in self.request.GET else False )

        if "page" in self.request.GET:
            self.current_pagination = ( int(self.request.GET["page"]) if "page" in self.request.GET else 1 )

        movie_filter_helper = MovieFilterHelper()
        movie_filter_helper.is_filtering = self.is_filter
        movie_filter_helper.selected_genres = self.filter_genre
        movie_filter_helper.selected_years = self.filter_years
        movie_filter_helper.selected_companies = self.filter_company
        movie_filter_helper.selected_keyword = self.keyword
        movie_filter_helper.only_subtitled = self.only_subtitled
        movie_filter_helper.current_order = self.filter_order
        movie_filter_helper.only_unlisted = self.only_unlisted
        self.local_variables["FilterHelper"] = movie_filter_helper

    def page_all(self):
        self.current_page = base.PAGE_MOVIES
        movies = []

        if self.is_filter:

            if not self.only_subtitled:
                movie_ids = HM.Movie.objects.all().values_list("pk", flat=True)
            else:
                movie_ids = HM.Movie.objects.filter(is_subtitled=True).values_list("pk", flat=True)

            if movie_ids and self.keyword:
                movie_ids = HM.Movie.objects.filter(pk__in=movie_ids, name__icontains=self.keyword).values_list("pk", flat=True)

            if movie_ids and self.filter_genre:
                movie_ids = HM.MovieGenre.objects.filter(genre__pk__in=self.filter_genre, movie__pk__in=movie_ids).values_list("movie__pk", flat=True)

            if movie_ids and self.filter_company:
                movie_ids = HM.MovieProductionCompany.objects.filter(production_company__pk__in=self.filter_company, movie__pk__in=movie_ids).values_list("movie__pk", flat=True)

            if movie_ids and self.filter_years:
                from django.db.models import Q
                queries = []

                for year in self.filter_years:
                    queries.append( Q(release_date__year=year) )

                query = queries.pop()
                for item in queries:
                    query |= item

                query &= Q(pk__in=movie_ids)

                movie_ids = HM.Movie.objects.filter(query).values_list("pk", flat=True)

            if movie_ids and self.only_unlisted:
                seen_list = HM.ViewedList.objects.filter(user=self.request.user).values_list("movie__pk", flat=True)
                pending_list = HM.PendingList.objects.filter(user=self.request.user).values_list("movie__pk", flat=True)
                movie_ids = HM.Movie.objects.filter(pk__in=movie_ids).exclude(pk__in=seen_list).exclude(pk__in=pending_list).values_list("pk", flat=True)

            movies = HM.Movie.objects.filter(pk__in=movie_ids)

            if self.filter_order != "standard":
                if self.filter_order == "duration":
                    movies = movies.order_by("-runtime")
                elif self.filter_order == "year":
                    movies = movies.order_by("-release_date")
                elif self.filter_order == "rating":
                    movies = movies.order_by("-vote_average")
                elif self.filter_order == "popularity":
                    movies = movies.order_by("-popularity")
            else:
                movies = movies.order_by("-pk")

        else:
            movies = HM.Movie.objects.all().order_by("-pk")

        total_results = movies.count()
        first = (self.current_pagination - 1) * RESULTS_PER_PAGE
        last = (first + (RESULTS_PER_PAGE) ) if (first + (RESULTS_PER_PAGE) ) < total_results else total_results

        movies = movies[first:last]

        self.local_variables["CurrentPage"] = self.current_pagination
        self.local_variables["TotalCount"] = total_results
        self.local_variables["IndexStart"] = first
        self.local_variables["IndexStop"] = last
        self.local_variables["HasNextPage"] = last < total_results
        self.local_variables["HasPreviousPage"] = first != 0

        self.local_variables["Movies"] = movies
        self.local_variables["Title"] = _("Toate Filmele Disponibile") if not self.is_filter else _("Cautare in Librarie")

        return self.render("pages/movie_loop.html")

    def page_filter_by_actor(self, actor):
        pass

    def page_filter_by_genre(self, genre):
        pass

    def page_filter_by_status(self, user):
        pass

    def page_movie_details(self, movie):

        if self.request.method == "POST" and self.request.POST.get("action") == "toggle_subtitles":
            movie.is_subtitled = (not movie.is_subtitled)
            movie.save()

        self.current_page = base.PAGE_MOVIE_SINGLE
        self.local_variables["Movie"] = movie
        self.local_variables["Title"] = _( "Filme > %s" ) % movie.name

        return self.render("pages/movie_single.html")