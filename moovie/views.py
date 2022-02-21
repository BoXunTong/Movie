# from __future__ import generator_stop
from django.shortcuts import render
from moovie.models import Movie, DirectorMovie, Review, Genre, Person, MovieGenre, ActorMovie

from moovie.models import ActorMovie, DirectorMovie

def index(request):
    return render(request, 'moovie/index.html', context={})

def contact_us(request):
    return render(request, 'moovie/contact.html', context = {})

def show_movie_profile(request, movie_id):
    context_dict = {}
    try:
        # is there a movie with this slug?
        movie = Movie.objects.get(id=movie_id)
        context_dict['movie'] = movie

        directors = getDirectorsForMovie(movie)
        context_dict['directors'] = directors

        stars = getActorsForMovie(movie)
        context_dict['stars'] = stars

        genres = getGenresForMovie(movie)
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

def about_us(request):
    return render(request, 'moovie/about.html', context = {})

def user_login(request):
    return render(request, 'moovie/login.html', context = {})

def user_signup(request):
    return render(request, 'moovie/signup.html', context = {})

# @login_required
def edit_profile(request):
    # this is the profile of the logged in user (with edit functionality)
    return render(request, 'moovie/edit_profile.html', context = {})

def getDirectorsForMovie(movie):
    directorMovies = DirectorMovie.objects.filter(movie_id=movie)
    directors = []
    for director in directorMovies:
        directors.append(Person.objects.get(person_id=director.person_id))
    return directors

def getActorsForMovie(movie):
    # do we need to limit this to only the 'top' actors?
    # how to determine 'top'?
    actorMovies = ActorMovie.objects.filter(movie_id=movie)
    actors = []
    for actor in actorMovies:
        actors.append(Person.objects.get(person_id=actor.person_id))
    return actors

def getGenresForMovie(movie):
    movieGenres = MovieGenre.objects.filter(movie_id=movie)
    genres = []
    for genre in movieGenres:
        genres.append(Genre.objects.get(name=genre.genre_name))


