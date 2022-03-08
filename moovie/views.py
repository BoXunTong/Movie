# from __future__ import generator_stop
from django.shortcuts import render
from django.views import View

from moovie.models import Movie, DirectorMovie, Review, Genre, Person, MovieGenre, ActorMovie

from moovie.models import ActorMovie, DirectorMovie


# Index view class
class IndexView(View):
    def get(self, request):
        context_dict = {}
        highest_rate_movie = Movie.objects.order_by('-average_rating')[0]
        movies_by_rating = Movie.objects.order_by('-average_rating')[1:5]
        movies_by_release = Movie.objects.order_by('-release_date')[:6]

        context_dict['highest_rate_movie'] = highest_rate_movie
        context_dict['movies_by_rating'] = movies_by_rating
        context_dict['movies_by_release'] = movies_by_release

        return render(request, 'moovie/index.html', context_dict)


def contact_us(request):
    return render(request, 'moovie/contact.html', context = {})

def show_movie_profile(request, movie_id):
    context_dict = {}
    try:
        # is there a movie with this slug?
        movie = Movie.objects.get(id=movie_id)
        context_dict['movie'] = movie

        directors = get_directors_for_movie(movie)
        context_dict['directors'] = directors

        stars = get_actors_for_movie(movie)
        context_dict['stars'] = stars

        genres = get_genres_for_movie(movie)
        context_dict['genres'] = genres

        reviews = Review.objects.filter(movie_id=movie)
        context_dict['reviews'] = reviews
        
    except Movie.DoesNotExist:
        context_dict['movie'] = None
        context_dict['directors'] = None
        context_dict['stars'] = None
        context_dict['genres'] = None
        context_dict['reviews'] = None

    return render(request, 'moovie/movie_profile.html', context=context_dict)

def show_search_result(request):
    return render(request, 'moovie/search_result.html', context = {})

def show_user_profile(request):
    # this is the publicly visible profile of any user
    return render(request, 'moovie/user_profile.html', context = {})

# About us view class
class AboutUsView(View):
    def get(self, request):
        return render(request, 'moovie/about.html', context={})


def user_login(request):
    return render(request, 'moovie/login.html', context = {})

def user_signup(request):
    return render(request, 'moovie/signup.html', context = {})

# @login_required
def edit_profile(request):
    # this is the profile of the logged in user (with edit functionality)
    return render(request, 'moovie/edit_profile.html', context = {})

def get_directors_for_movie(movie):
    directorMovies = DirectorMovie.objects.filter(movie_id=movie)
    directors = []
    for director_movie in directorMovies:
        person_id = director_movie.person_id.id
        directors.append(Person.objects.get(id=person_id))
    return directors

def get_actors_for_movie(movie):
    # do we need to limit this to only the 'top' actors?
    # how to determine 'top'?
    actorMovies = ActorMovie.objects.filter(movie_id=movie)
    actors = []
    for actor_movie in actorMovies:
        person_id = actor_movie.person_id.id
        actors.append(Person.objects.get(id=person_id))
    return actors

def get_genres_for_movie(movie):
    movieGenres = MovieGenre.objects.filter(movie_id=movie)
    genres = []
    for movie_genre in movieGenres:
        # genres.append(Genre.objects.get(name=genre.genre_name))
        genres.append(movie_genre.genre_name)
    return genres


