
REQUEST_LIMIT_PER_BATCH = 15


def throttle_request_increase(current_limit):
    """
    Increases the last connection queue count, once it reaches the limit, the application is put to sleep and the counter is reset
    :param current_limit: current limit, as previously set
    :return: int - new limit
    """
    current_limit += 1

    if current_limit >= REQUEST_LIMIT_PER_BATCH:
        import time
        print "Sleeping for 8 seconds after %s requests" % current_limit
        time.sleep(8)

        return 0

    return current_limit


def process_import_file(request, manual=False):
    """
    This will process the import file (JSON), loop trough each entry and fill the database will all the requested content
    :param request: Request object
    :return: JSON-Encoded Response
    """
    from django.http import HttpResponse
    import tmdbsimple as tmdb
    import json
    from HomeCloud.settings import BASE_DIR
    import home.models as HM
    import datetime

    tmdb.API_KEY = "8a6ec3db37cb0821ed4d584454cba913"
    results = json.load( open( BASE_DIR + '/tools/explorer_results.json') )
    import_count = 0
    skip_count = 0
    process_count = 0
    added_movies_list = []

    api_requests_done = 0

    if results and "movies" in results and len(results["movies"]) > 0:
        for imnmovie, vals in results["movies"].iteritems():
            for movie_single, movie_vals in vals.iteritems():
                try:
                    process_count += 1
                    print "Now processing: %s" % imnmovie

                    if HM.Movie.objects.filter(file_name=movie_vals["file"], local_path=movie_vals["directory"]).count() == 0:

                        search = tmdb.Search()
                        search.movie(query=imnmovie)

                        for s in search.results:
                            added_movies_list.append( s["title"] )
                            import_count += 1

                            tmdb_movie_single = tmdb.Movies(s["id"])
                            api_requests_done = throttle_request_increase(api_requests_done)
                            s = tmdb_movie_single.info()

                            try:
                                release_date = datetime.datetime.strptime(s["release_date"], "%Y-%m-%d").date() if s["release_date"] else datetime.datetime.now()
                            except:
                                release_date = datetime.datetime.now()

                            # add the primary movies details
                            movie = HM.Movie.objects.create(
                                name = s["title"],
                                file_name = movie_vals["file"],
                                local_path = movie_vals["directory"],
                                is_subtitled = bool(movie_vals["subtitle"]),
                                tmdb_id = s["id"],
                                imdb_id = s["imdb_id"],
                                overview = s["overview"] if ( "overview" in s and s["overview"] ) else "",
                                popularity = s["popularity"],
                                release_date = release_date,
                                revenue = s["revenue"],
                                runtime = s["runtime"],
                                tagline = s["tagline"] if ( "tagline" in s and s["tagline"] ) else "",
                                vote_average = s["vote_average"],
                                poster_image = s["poster_path"] if ( "poster_path" in s and s["poster_path"] ) else "",
                                backdrop_image = s["backdrop_path"] if ( "backdrop_path" in s and s["backdrop_path"] ) else "",
                                youtube_video_code = ""
                            )

                            tmdb_movie = tmdb.Movies(s["id"])
                            tmdb_movie.credits()
                            api_requests_done = throttle_request_increase(api_requests_done)

                            # add movie cast
                            if tmdb_movie.cast:
                                print "Processing a cast of %d actors" % len(tmdb_movie.cast)
                                for cast in tmdb_movie.cast:

                                    if HM.Actor.objects.filter(tmdb_id=cast["id"]).count() == 0:
                                        tmdb_actor = tmdb.People(cast["id"])
                                        tmdb_actor.info()
                                        api_requests_done = throttle_request_increase(api_requests_done)

                                        try:
                                            birthday = datetime.datetime.strptime(tmdb_actor.birthday, "%Y-%m-%d").date() if tmdb_actor.birthday else None
                                        except:
                                            birthday = None

                                        try:
                                            deathday = datetime.datetime.strptime(tmdb_actor.deathday, "%Y-%m-%d").date() if tmdb_actor.deathday else None
                                        except:
                                            deathday = None

                                        actor = HM.Actor.objects.create(
                                            name = tmdb_actor.name,
                                            birthday = birthday,
                                            tmdb_id = tmdb_actor.id,
                                            death = deathday,
                                            aliases = json.dumps(tmdb_actor.also_known_as) if tmdb_actor.also_known_as else "{}",
                                            biography = tmdb_actor.biography if tmdb_actor.biography else "",
                                            place_of_birth = tmdb_actor.place_of_birth if tmdb_actor.place_of_birth else "",
                                            homepage = tmdb_actor.homepage if tmdb_actor.homepage else "",
                                            profile_image = tmdb_actor.profile_path if tmdb_actor.profile_path else ""
                                        )
                                    else:
                                        actor = HM.Actor.objects.get(tmdb_id=cast["id"])

                                    HM.MovieActor.objects.create(movie=movie, actor=actor)

                                    HM.Cast.objects.create(
                                        name = cast["character"] if "character" in cast else "",
                                        cast_id = cast["cast_id"],
                                        actor = actor,
                                        movie = movie,
                                        credit = cast["credit_id"],
                                        order = cast["order"],
                                        profile_image = cast["profile_path"] if ( "profile_path" in cast and cast["profile_path"] ) else ""
                                    )

                            # add movie trailers
                            tmdb_movie_videos = tmdb.Movies(s["id"])
                            tmdb_movie_videos.videos()
                            api_requests_done = throttle_request_increase(api_requests_done)

                            if tmdb_movie_videos.results:
                                for result in tmdb_movie_videos.results:
                                    if str(result["type"]).lower() == "trailer" and str(result["site"]).lower() == "youtube":
                                        if str(result["iso_639_1"]) == "en":
                                            movie.youtube_video_code = result["key"]
                                            movie.save()

                            # load and add reviews
                            tmdb_movie_reviews = tmdb.Movies(s["id"])
                            tmdb_movie_reviews.reviews()
                            api_requests_done = throttle_request_increase(api_requests_done)

                            if tmdb_movie_reviews.results:
                                for single_review in tmdb_movie_reviews.results:
                                    try:
                                        HM.Review.objects.create(
                                            author = single_review["author"] if ("author" in single_review and single_review["author"]) else "",
                                            content = single_review["content"] if ("content" in single_review and single_review["content"]) else "",
                                            url = single_review["url"] if ("url" in single_review and single_review["url"]) else "",
                                            movie = movie
                                        )
                                    except Exception:
                                        pass

                            # add the genres
                            if "genres" in s:
                                for genre in s["genres"]:
                                    try:
                                        genre_object = HM.Genre.objects.get(name=genre["name"])
                                    except HM.Genre.DoesNotExist:
                                        genre_object = HM.Genre.objects.create(name=genre["name"])

                                    HM.MovieGenre.objects.create(genre=genre_object, movie=movie)

                            # add production companies
                            if "production_companies" in s:
                                for pcompany in s["production_companies"]:
                                    try:
                                        pc_object = HM.ProductionCompany.objects.get(name=pcompany["name"])
                                    except HM.ProductionCompany.DoesNotExist:
                                        pc_object = HM.ProductionCompany.objects.create(name=pcompany["name"])

                                    HM.MovieProductionCompany.objects.create(production_company=pc_object, movie=movie)

                            break  # we only need one result here

                    else:
                        skip_count += 1
                        existing_movie = HM.Movie.objects.get(file_name=movie_vals["file"], local_path=movie_vals["directory"])
                        existing_movie.is_subtitled = bool(movie_vals["subtitle"])
                        existing_movie.save()

                        print "Skipping %s" % imnmovie

                except Exception:
                    print "had exception for movie: %s" % imnmovie


    data = { "total_entries": process_count, "skip_count": skip_count, "import_count": import_count, "movies": added_movies_list  }
    return HttpResponse(json.dumps(data), content_type="application/json")