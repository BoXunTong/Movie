
# from __future__ import generator_stop
from tkinter import messagebox, mainloop
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect, reverse
from moovie.models import *
from moovie.forms import *
from django.http import HttpResponse


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

            # messages.success(request, "Congratulation! Welcome to Moovie!")
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
            mainloop()
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
    # m=User.objects.get(USERNAME=request.POST['username'])
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
                mainloop()
                # messages.success(request, "Login Successfully, Welcome!")
                print("Login OK!")
                login(request, user)
                return redirect(reverse('moovie:index'))
            else:
                # An inactive account was used - no logging in!
                # messages.error(request, "Something Wrong, please try again later...")
                messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
                mainloop()
                # return HttpResponse("Your moovie account is disabled.")
                return redirect(reverse('moovie:login'))
        else:
            # Bad login details were provided. So we can't log the user in.
            # print(f"Invalid login details: {username}, {password}")
            detail_is_invalid = True,
            # messages.error(request, "Something Wrong, please try again later...")
            messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
            mainloop()
            # return HttpResponse("Invalid login details supplied.")
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
    return render(request, 'moovie/contact.html', context=context_dict)


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

        if request.user.is_authenticated:
            context_dict['already_added_to_watchlist'] = MovieToWatch.objects.filter(username=request.user, movie_id= movie_id).count()

        reviews_with_user_info = get_reviews_with_user_info_for_movie(movie)
        context_dict['reviews_with_user_info'] = reviews_with_user_info

        context_dict['form'] = get_users_review_if_exists(request, movie)

    except Movie.DoesNotExist:
        context_dict['movie'] = None
        context_dict['directors'] = None
        context_dict['stars'] = None
        context_dict['genres'] = None
        context_dict['reviews_with_user_info'] = None

    return render(request, 'moovie/movie_profile.html', context=context_dict)


def get_movie_from_person(search_terms, keyword, max_results=0):
    person_list_name = []
    person_list_surname = []
    movie_list = []
    if search_terms:
        person_list_name = Person.objects.filter(name__icontains=search_terms)
        person_list_surname = Person.objects.filter(surname__icontains=search_terms)
    for person_name in person_list_name:
        if keyword == 2:
            directors = DirectorMovie.objects.filter(person_id=person_name)
            for director in directors:
                movie_id = director.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))
        elif keyword == 3:
            actors = ActorMovie.objects.filter(person_id=person_name)
            for actor in actors:
                movie_id = actor.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))

    for person_surname in person_list_surname:
        if keyword == 2:
            directors = DirectorMovie.objects.filter(person_id=person_surname)
            for director in directors:
                movie_id = director.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))
        elif keyword == 3:
            actors = ActorMovie.objects.filter(person_id=person_surname)
            print(actors)
            for actor in actors:
                movie_id = actor.movie_id.id
                movie_list.append(Movie.objects.get(id=movie_id))
    movie_list = set(movie_list)
    return movie_list   

'''
def get_movie_from_genre(search_terms):
    movie_list = []
    print(search_terms)
    if search_terms:
        movie_id_list = MovieGenre.objects.filter(genre_name=search_terms)
    for movie_id in movie_id_list:
        movie_list.append(Movie.objects.get(id=movie_id))
    return movie_list
''' 


def get_movie_list(search_terms, max_results=0):
    movie_list = []
    if search_terms:
        movie_list = Movie.objects.filter(title__icontains=search_terms)
    if max_results > 0:
        if len(movie_list) > max_results:
            movie_list = movie_list[:max_results]
    return movie_list

def run_query(search_terms, keyword):
    search_results = []
    if(keyword == 1):
        search_results = get_movie_list(search_terms)
    else:
        search_results = get_movie_from_person(search_terms,keyword)
    '''
    else:
        search_results = get_movie_from_genre(search_terms)
    '''
    results = []

    for result in search_results:
        director = get_directors_for_movie(result)
        director = str(director)
        director = director[12:-2]
        results.append({
            'id':result.id,
            'title':result.title,
            'image':result.image,
            'director':director,
            'release_date':result.release_date
        })
    return results

def search_tag(request, search_type, query):
    context_dict = {}
    
    if search_type == 'Genre':
        keyword = 1
    elif search_type == 'Director':
        keyword = 2
    elif search_type == 'Actor':
        keyword = 3

    if query:
        context_dict['result_list'] = run_query(query, keyword)
        context_dict['query'] = query 
    return render(request, 'moovie/search_result.html', context=context_dict)

def show_search_result(request):
    context_dict = {}
    if request.method == 'POST':
        query = request.POST['query'].strip()
        keyword = request.POST['search_dropdown']
        if keyword == 'Title':
            keyword = 1
        elif keyword == 'Director':
            keyword = 2
        elif keyword == 'Actor':
            keyword = 3
        '''
        else:
            keyword = 4
        '''
        if query:
            context_dict['result_list'] = run_query(query, keyword)
            #context_dict['result_list'] = run_query(query)
            context_dict['query'] = query 
    return render(request, 'moovie/search_result.html', context=context_dict)

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


def get_reviews_with_user_info_for_movie(movie):
    reviews = Review.objects.filter(movie_id=movie)
    reviews_with_user_info = []
    for review in reviews:
        user_profile = UserProfile.objects.get(user=review.username)
        reviews_with_user_info.append({'review': review, 'user': user_profile})
    return reviews_with_user_info


def get_users_review_if_exists(request, movie):
    try:
        if request.user.is_authenticated:
            review = Review.objects.get(movie_id=movie, username=request.user)
            review_form = ReviewForm(instance=review)
            return review_form
        else:
            ReviewForm()
    except Review.DoesNotExist:
        return ReviewForm()


def add_review(request, movie_id):
    form = ReviewForm()

    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username'))
        user_has_an_existing_comment = False
        if Review.objects.filter(movie_id=movie_id, username=user).count() == 0:
            form = ReviewForm(request.POST)
        else:
            form = ReviewForm(request.POST, instance=Review.objects.get(movie_id=movie_id, username=user))
            user_has_an_existing_comment = True

        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = Movie.objects.get(id=movie_id)
            review.username = user

            calculate_and_save_new_rating(movie_id, review, user_has_an_existing_comment)
            review.save()

            return redirect(reverse('moovie:show_movie_profile',
                                    kwargs={'movie_id':
                                                movie_id}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'movie_id': movie_id}
    return render(request, 'moovie/movie_profile.html', context=context_dict)


def calculate_and_save_new_rating(movie_id, review, user_has_an_existing_comment):
    movie = Movie.objects.get(id=movie_id)
    review_count = Review.objects.filter(movie_id=movie_id).count()

    if user_has_an_existing_comment:
        existing_review = Review.objects.get(movie_id=movie_id, username=review.username)
        movie.average_rating = (
                                           movie.average_rating * review_count - existing_review.rating + review.rating) / review_count
    else:
        movie.average_rating = (movie.average_rating * review_count + review.rating) / (review_count + 1)

    movie.save() 

class AddToWatchlistView(View):
    def get(self, request):
        movie_id = request.GET['movie_id']
        MovieToWatch.objects.create(username=request.user, movie_id= Movie.objects.get(id=movie_id))
        
        return HttpResponse()

class RemoveFromWatchlistView(View):
    def get(self, request):
        movie_id = request.GET['movie_id']
        MovieToWatch.objects.get(username=request.user, movie_id= Movie.objects.get(id=movie_id)).delete()
        
        return HttpResponse()
