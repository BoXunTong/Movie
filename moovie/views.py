# from __future__ import generator_stop
from django.shortcuts import render, redirect, reverse
from moovie.models import Movie, DirectorMovie, Review, Genre, Person, MovieGenre, ActorMovie, User, UserProfile
from moovie.forms import ReviewForm, ContactMessageForm

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
    form = ContactMessageForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save()
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('moovie:contact_us'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    context_dict = {'form': form}
    return render(request, 'moovie/contact.html', context = context_dict)

def show_movie_profile(request, movie_id):
    context_dict = {}
    try:
        movie = Movie.objects.get(id=movie_id)
        context_dict['movie'] = movie

        directors = get_directors_for_movie(movie)
        context_dict['directors'] = directors

        stars = get_actors_for_movie(movie)
        context_dict['stars'] = stars

        genres = get_genres_for_movie(movie)
        context_dict['genres'] = genres

        reviews_with_user_info = get_reviews_with_user_info_for_movie(movie)
        context_dict['reviews_with_user_info'] = reviews_with_user_info

        context_dict['form'] = ReviewForm()
        
    except Movie.DoesNotExist:
        context_dict['movie'] = None
        context_dict['directors'] = None
        context_dict['stars'] = None
        context_dict['genres'] = None
        context_dict['reviews_with_user_info'] = None

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

def get_reviews_with_user_info_for_movie(movie):
    reviews = Review.objects.filter(movie_id=movie)
    reviews_with_user_info = []
    for review in reviews:
        user_profile = UserProfile.objects.get(user=review.username)
        reviews_with_user_info.append({'review':review, 'user': user_profile})
    return reviews_with_user_info

def add_review(request, movie_id):
    form = ReviewForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            
            review = form.save(commit=False)
            review.movie_id = Movie.objects.get(id=movie_id)
            review.username = User.objects.get(username=request.POST.get('username'))

            calculate_and_save_new_rating(movie_id, review.rating)
            review.save()

            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('moovie:show_movie_profile',
                                        kwargs={'movie_id':
                                                movie_id}))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    context_dict = {'form': form, 'movie_id': movie_id}
    return render(request, 'moovie/movie_profile.html', context = context_dict)

def calculate_and_save_new_rating(movie_id, new_rating):
    movie = Movie.objects.get(id=movie_id)
    review_count = Review.objects.filter(movie_id=movie_id).count()
    movie.average_rating = (movie.average_rating * review_count + new_rating) / (review_count + 1)
    movie.save() 
