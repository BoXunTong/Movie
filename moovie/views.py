# from __future__ import generator_stop
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from moovie.forms import UserForm, UserProfileForm
from moovie.models import Movie, DirectorMovie, Review, Genre, Person, MovieGenre, ActorMovie, User
from moovie.models import ActorMovie, DirectorMovie
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from tkinter import messagebox #弹窗库
# Index view class
class IndexView(View):
    def get(self, request):
        context_dict = {}
        highest_rate_movie = Movie.objects.order_by('-average_rating')[0]
        movies_by_rating = Movie.objects.order_by('-average_rating')[1:5]
        movies_by_release = Movie.objects.order_by('-release_date')[:5]

        context_dict['highest_rate_movie'] = highest_rate_movie
        context_dict['movies_by_rating'] = movies_by_rating
        context_dict['movies_by_release'] = movies_by_release

        return render(request, 'moovie/index.html', context_dict)


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.

    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.

        user_form = UserForm(request.POST)
        # profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        # if user_form.is_valid() and profile_form.is_valid():
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            #messages.success(request, "Congratulation! Welcome to Moovie!")
            messagebox.showinfo("Welcome", "Now you are one of us!")
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.

            # profile = profile_form.save(commit=False)
            # profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.

            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.

            # profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            return redirect(reverse('moovie:index'))
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
            # print(user_form.errors, profile_form.errors)
            print(user_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.

        user_form = UserForm()
        # profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request, 'moovie/register.html',
                  # context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
                  context={'user_form': user_form, 'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    #m=User.objects.get(USERNAME=request.POST['username'])
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                messagebox.showinfo("Welecome", "Login successfully!")
                #messages.success(request, "Login Successfully, Welcome!")
                print("Login OK!")
                login(request, user)
                return redirect(reverse('moovie:index'))
            else:
                # An inactive account was used - no logging in!
                #messages.error(request, "Something Wrong, please try again later...")
                messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
                #return HttpResponse("Your moovie account is disabled.")
                return redirect(reverse('moovie:login'))
        else:
            # Bad login details were provided. So we can't log the user in.
            # print(f"Invalid login details: {username}, {password}")
            detail_is_invalid = True,
            #messages.error(request, "Something Wrong, please try again later...")
            messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
            #return HttpResponse("Invalid login details supplied.")
            return redirect(reverse('moovie:login'))

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'moovie/login.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('moovie:index'))


def contact_us(request):
    return render(request, 'moovie/contact.html', context={})


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
    return render(request, 'moovie/search_result.html', context={})


def show_user_profile(request):
    # this is the publicly visible profile of any user
    return render(request, 'moovie/user_profile.html', context={})


# About us view class
class AboutUsView(View):
    def get(self, request):
        return render(request, 'moovie/about.html', context={})


# @login_required
def edit_profile(request):
    # this is the profile of the logged in user (with edit functionality)
    return render(request, 'moovie/edit_profile.html', context={})


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
