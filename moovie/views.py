# from __future__ import generator_stop
from ast import keyword
from xmlrpc.server import SimpleXMLRPCDispatcher
from django.shortcuts import render
from moovie.models import Movie, DirectorMovie, Review, Genre, Person, MovieGenre, ActorMovie

from moovie.models import ActorMovie, DirectorMovie

def index(request):
    context_dict = {}
    
    # movies_by_rating = Movie.objects.all()
    movies_by_rating = Movie.objects.order_by('-average_rating')[:5]
    movies_by_release = Movie.objects.order_by('-release_date')[:5]

    context_dict['movies_by_rating'] = movies_by_rating
    context_dict['movies_by_release'] = movies_by_release

    return render(request, 'moovie/index.html', context=context_dict)

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

'''
def show_search_result(request, movie_id):
    context_dict = {}
    try:
        movie = Movie.objects.get(id=movie_id)
        context_dict['movie'] = movie
        directors = get_directors_for_movie(movie)
        context_dict['directors'] = directors

    except Movie.DoesNotExist:
        context_dict['movie'] = None
        context_dict['directors'] = None

    return render(request, 'moovie/search_result.html', context = context_dict)
'''
def get_movie_from_person(keyword, max_results=0, starts_with=''):
    person_list = []
    movie_list = []
    if starts_with:
        person_list = Person.objects.filter(name__istartswith=starts_with)
    for person in person_list:
        if keyword == 'director':
            diretors = DirectorMovie.objects.filter(person_id=person)
            for director in directors:
                movie_id = director.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))
        elif keyword == 'actor':
            actors = ActorMovie.objects.filter(person_id=person)
            for actor in actors:
                movie_id = actor.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))
    return movie_list       

def get_movie_list(max_results=0, starts_with=''):
    movie_list = []
    if starts_with:
        movie_list = Movie.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(movie_list) > max_results:
            movie_list = movie_list[:max_results]
    return movie_list

def run_query(search_terms,keyword):
    if(keyword == 'movie'):
        search_results = get_movie_list()
    elif(keyword == 'director' | keyword == 'actor'):
        search_results = get_movie_from_person(keyword)
    results = []
    for result in search_results:
        results.append({
            'title':result['movie'],
            'image':result['poster'],
            'director':result['director'],
            'release_date':result['release_date']
        })
    return


def show_search_result(request):
    context_dict = {}
    if request.method == 'POST':
        query = request.POST['query'].strip()
        keyword = request.POST['keyword'].strip()
        if query:
            context_dict['result_list'] = run_query(query,keyword)
            context_dict['query'] = query
    return render(request, 'moovie/search_result.html', context_dict)

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

