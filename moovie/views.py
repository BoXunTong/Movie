# from __future__ import generator_stop
from platform import release
from tkinter import messagebox, mainloop
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.shortcuts import render, redirect, reverse
from moovie.models import *
from moovie.forms import *
from tkinter import *
from django.http import HttpResponse
from django.contrib import messages


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
            messages.success(request, "Congratulation! Welcome to Moovie!")

            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # messagebox.showinfo("Welcome", "Now you are one of us!")
            # mainloop()
            # root.destroy()
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
            # registered = True
            return redirect(reverse('moovie:login'))
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            messages.error(request, "Something Wrong, please try again later...")
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
                # messagebox.showinfo("Welecome", "Login successfully!")
                # mainloop()
                # messages.success(request, "Login Successfully, Welcome!")
                login(request, user)
                return redirect(reverse('moovie:index'))
            else:
                # An inactive account was used - no logging in!
                # messages.error(request, "Something Wrong, please try again later...")
                # messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
                # mainloop()
                # root.destroy()
                # return HttpResponse("Your moovie account is disabled.")
                messages.error(request, 'The user name or password is incorrect')
                return redirect(reverse('moovie:login'))
        else:
            # Bad login details were provided. So we can't log the user in.
            # print(f"Invalid login details: {username}, {password}")
            detail_is_invalid = True,
            messages.error(request, "Something Wrong, please try again later...")
            # messagebox.showerror("Sorry！", "Something Wrong, please try again later...")
            # return HttpResponse("Invalid login details supplied.")
            return redirect(reverse('moovie:login'))

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # root.destroy()
        return render(request, 'moovie/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('moovie:index'))


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
    if (keyword == 1):
        search_results = get_movie_list(search_terms)
    else:
        search_results = get_movie_from_person(search_terms, keyword)
    results = []

    for result in search_results:
        movie_view = MovieView()
        director = movie_view.get_directors_for_movie(result)
        director = str(director)
        director = director[12:-2]
        genre = movie_view.get_genres_for_movie(result)
        genre = str(genre)
        genre = genre[9:18] + genre[28:36]
        release_date = str(result.release_date)
        release_date = release_date[:-15]
        results.append({
            'id':result.id,
            'title':result.title,
            'image':result.image,
            'director':director,
            'release_date':release_date,
            'genre':genre
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
        if query:
            context_dict['result_list'] = run_query(query, keyword)
            # context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
    return render(request, 'moovie/search_result.html', context=context_dict)



def show_user_profile(request, username):
    context_dict = {}
    try:
        thisuser = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=thisuser.id)
        context_dict['user_profile'] = user_profile

        reviews_with_movies = get_reviews_for_user(thisuser)
        context_dict['reviews_with_movies'] = reviews_with_movies

        wishlist = get_wishlist_for_user(thisuser)
        context_dict['wishlist'] = wishlist

    except (User.DoesNotExist, UserProfile.DoesNotExist):
        context_dict['user'] = None
        context_dict['user_profile'] = None
        context_dict['reviews_with_movies'] = None
        context_dict['wishlist'] = None

    return render(request, 'moovie/user_profile.html', context = context_dict)

def get_reviews_for_user(user):
    reviews = Review.objects.filter(username=user)
    reviews_with_movies = []
    for review in reviews:
        movie_id = review.movie_id
        reviews_with_movies.append({'review':review, 'movie':movie_id})
    return reviews_with_movies

def get_wishlist_for_user(user):
    movies_to_watch = MovieToWatch.objects.filter(username=user)
    wishlist = []
    for mov2w in movies_to_watch:
        wishlist.append(mov2w.movie_id)
    return wishlist

# About us view class
class AboutUsView(View):
    def get(self, request):
        return render(request, 'moovie/about.html', context={})

# @login_required
def edit_profile(request):
    # this is the profile of the logged in user (with edit functionality)
    return render(request, 'moovie/edit_profile.html', context = {})


class ReviewView(View):
    def post(self, request, movie_id):
        #gets user model.
        user = User.objects.get(username=request.POST.get('username'))
        #holds whether the user already has a review for the movie.
        user_has_an_existing_comment = False

        #checks if there is a review that the user has made previously for the movie.
        if Review.objects.filter(movie_id=movie_id, username=user).count() == 0:
            form = ReviewForm(request.POST)
        else:
            form = ReviewForm(request.POST, instance=Review.objects.get(movie_id=movie_id, username=user))
            user_has_an_existing_comment = True

        #checks if the form is valid.
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = Movie.objects.get(id=movie_id)
            review.username = user

            #calculates the new average rating of the movie considering if the review is new or the user is editing an existing review.
            self.calculate_and_save_new_average_rating(movie_id, review, user_has_an_existing_comment)
            review.save()
            messages.success(request, "Thank you for your review!", fail_silently=True)

            return redirect(reverse('moovie:show_movie_profile', kwargs={'movie_id': movie_id}))
        else:
            messages.error(request, "Something went wrong with the form!", fail_silently=True)
            print(form.errors)

        context_dict = {'form': form, 'movie_id': movie_id}
        return render(request, 'moovie/movie_profile.html', context=context_dict)

    def calculate_and_save_new_average_rating(self, movie_id, review, user_has_an_existing_comment):
        #gets movie model.
        movie = Movie.objects.get(id=movie_id)
        #counts total number of reviews made for the movie.
        review_count = Review.objects.filter(movie_id=movie_id).count()

        #checks if the user has an existing comment for the movie.
        if user_has_an_existing_comment:
            #gets the existing comment.
            existing_review = Review.objects.get(movie_id=movie_id, username=review.username)
            #calculates the new average rating by subtracting the existing rating and adding the new one.
            movie.average_rating = (movie.average_rating * review_count - existing_review.rating + review.rating) / review_count
        else:
            #calculates the new average rating by adding the new one.
            movie.average_rating = (movie.average_rating * review_count + review.rating) / (review_count + 1)

        movie.save()

class MovieView(View):
    #shows a movie's profile page with the necessary information.
    def get(self, request, movie_id):
        context_dict = {}
        try:
            #gets movie model.
            movie = Movie.objects.get(id=movie_id)
            context_dict['movie'] = movie

            #gets the directors of the movie.
            directors = self.get_directors_for_movie(movie)
            context_dict['directors'] = directors

            #gets the actors of the movie.
            stars = self.get_actors_for_movie(movie)
            context_dict['stars'] = stars

            #gets the genres of the movie.
            genres = self.get_genres_for_movie(movie)
            context_dict['genres'] = genres

            #gets whether the user added the movie to his/her watchlist before, if authenticated.
            if request.user.is_authenticated:
                context_dict['already_added_to_watchlist'] = MovieToWatch.objects.filter(username=request.user, movie_id= movie_id).count()

            #gets all the reviews made for the movie with their user information.
            reviews_with_user_info = self.get_reviews_with_user_info_for_movie(movie)
            context_dict['reviews_with_user_info'] = reviews_with_user_info

            #gets the user's existing review if exists.
            context_dict['form'] = self.get_existing_review_if_exists(request, movie)

        except Movie.DoesNotExist:
            context_dict['movie'] = None
            context_dict['directors'] = None
            context_dict['stars'] = None
            context_dict['genres'] = None
            context_dict['reviews_with_user_info'] = None
            messages.error(request, "The movie cannot be found!", fail_silently=True)

        return render(request, 'moovie/movie_profile.html', context=context_dict)

    #gets directors of a given movie.
    def get_directors_for_movie(self, movie):
        #gets Director-Movie records for the movie.
        directorMovies = DirectorMovie.objects.filter(movie_id=movie)
        directors = []

        #finds directors for each Director-Movie record.
        for director_movie in directorMovies:
            person_id = director_movie.person_id.id
            directors.append(Person.objects.get(id=person_id))
        return directors

    #gets actors of a given movie.
    def get_actors_for_movie(self, movie):
        #gets Actor-Movie records for the movie.
        actorMovies = ActorMovie.objects.filter(movie_id=movie)
        actors = []

        #finds actors for each Actor-Movie record.
        for actor_movie in actorMovies:
            person_id = actor_movie.person_id.id
            actors.append(Person.objects.get(id=person_id))
        return actors

    #gets genres of a given movie.
    def get_genres_for_movie(self, movie):
        #gets Movie-Genre records for the movie.
        movieGenres = MovieGenre.objects.filter(movie_id=movie)
        genres = []

        #finds genres for each Movie-Genre record.
        for movie_genre in movieGenres:
            genres.append(movie_genre.genre_name)
        return genres

    #gets all the reviews of a given movie with their user information.
    def get_reviews_with_user_info_for_movie(self, movie):
        #gets the reviews.
        reviews = Review.objects.filter(movie_id=movie)
        reviews_with_user_info = []

        #find user information for each review.
        for review in reviews:
            user_profile = UserProfile.objects.get(user=review.username)
            reviews_with_user_info.append({'review': review, 'user': user_profile})
        return reviews_with_user_info

    #gets the user's review for a movie if exists.
    def get_existing_review_if_exists(self, request, movie):
        try:
            #gets the review and creates a review form with the information if the user is auhenticated.
            if request.user.is_authenticated:
                review = Review.objects.get(movie_id=movie, username=request.user)
                review_form = ReviewForm(instance=review)
                return review_form
            else:
                ReviewForm()
        except Review.DoesNotExist:
            return ReviewForm()


class ContactUsView(View):
    #shows the page.
    def get(self, request):
        form = ContactMessageForm()

        context_dict = {'form': form}
        return render(request, 'moovie/contact.html', context=context_dict)

    #saves a new message directly into the database.
    def post(self, request):
        form = ContactMessageForm(request.POST)

        #checks if the form is valid.
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message!", fail_silently=True)
            return redirect(reverse('moovie:contact_us'))
        else:
            messages.error(request, "Something went wrong with the from!", fail_silently=True)
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'moovie/contact.html', context=context_dict)

class AddMovieView(View):
    #shows the page.
    @method_decorator(staff_member_required)
    def get(self, request):
        movie_form = AddMovieForm()
        director_form = AddDirectorForm()
        actor_form = AddActorForm()
        genre_form = AddGenreForm()

        context_dict = { 'movie_form': movie_form, 'director_form': director_form, 'actor_form': actor_form, 'genre_form': genre_form }
        return render(request, 'moovie/add_movie.html', context=context_dict)

    #saves a new movie directly into the database.
    @method_decorator(staff_member_required)
    def post(self, request):
        movie_form = AddMovieForm(request.POST, request.FILES)
        director_form = AddDirectorForm(request.POST)
        actor_form = AddActorForm(request.POST)
        genre_form = AddGenreForm(request.POST)

        try:
            #checks if the forms are valid.
            if movie_form.is_valid() and director_form.is_valid() and actor_form.is_valid() and genre_form.is_valid():
                movie = movie_form.save()
                self.add_director_to_movie(director_form, movie)
                self.add_actor_to_movie(actor_form, movie)
                self.add_genre_to_movie(genre_form, movie)

                messages.success(request, "Movie added!", fail_silently=True)
                return redirect(reverse('moovie:add_movie'))
            else:
                messages.error(request, "Something went wrong with the from!", fail_silently=True)
                print(movie_form.errors)
                print(director_form.errors)
                print(actor_form.errors)
                print(genre_form.errors)
        except Exception as ex:
            message = ex.args
            messages.error(request, message, fail_silently=True)

        context_dict = { 'movie_form': movie_form, 'director_form': director_form, 'actor_form': actor_form, 'genre_form': genre_form }
        return render(request, 'moovie/add_movie.html', context=context_dict)

    #adds directors to a movie.
    def add_director_to_movie(self, director_form, movie):
        #checks if both fields have commas.
        if ((',' in director_form.cleaned_data['director_name'] and ',' not in director_form.cleaned_data['director_surname']) 
            or (',' not in director_form.cleaned_data['director_name'] and ',' in director_form.cleaned_data['director_surname'])):
            raise Exception('There should be commas in both director name and surname!')

        #splits multiple director names and surnames.        
        director_names = director_form.cleaned_data['director_name'].split(',')
        director_surnames = director_form.cleaned_data['director_surname'].split(',')

        #checks if there are equal number of director names and surnames.
        if len(director_names) != len(director_surnames):
            raise Exception('The number of director names and surname should be the same!')
        
        #saves information for each name.
        for i in range(len(director_names)):
            person = Person.objects.get_or_create(name=director_names[i].strip(), surname=director_surnames[i].strip(), person_type='Director')[0]
            DirectorMovie.objects.create(movie_id=movie, person_id=person)

    #adds actor to a movie.
    def add_actor_to_movie(self, actor_form, movie):
        #checks if both fields have commas.
        if ((',' in actor_form.cleaned_data['actor_name'] and ',' not in actor_form.cleaned_data['actor_surname']) 
            or (',' not in actor_form.cleaned_data['actor_name'] and ',' in actor_form.cleaned_data['actor_surname'])):
            raise Exception('There should be commas in both actor name and surname!')

        #splits multiple actor names and surnames.        
        actor_names = actor_form.cleaned_data['actor_name'].split(',')
        actor_surnames = actor_form.cleaned_data['actor_surname'].split(',')

        #checks if there are equal number of actor names and surnames.
        if len(actor_names) != len(actor_surnames):
            raise Exception('The number of actor names and surname should be the same!')
        
        #saves information for each name.
        for i in range(len(actor_names)):
            person = Person.objects.get_or_create(name=actor_names[i].strip(), surname=actor_surnames[i].strip(), person_type='Actor')[0]
            ActorMovie.objects.create(movie_id=movie, person_id=person)

    #adds genre to a movie.
    def add_genre_to_movie(self, genre_form, movie):

        #splits multiple genres.        
        genres = genre_form.cleaned_data['genre_name'].split(',')
        
        #saves information for each genre.
        for genre_name in genres:
            genre = Genre.objects.get_or_create(name=genre_name.strip())[0]
            MovieGenre.objects.create(genre_name=genre, movie_id=movie)

class AddToWatchlistView(View):
    #adds a movie to the user's watchlist.
    def get(self, request, movie_id):
        MovieToWatch.objects.create(username=request.user, movie_id= Movie.objects.get(id=movie_id))
        messages.success(request, "The movie is added to your watchlist!", fail_silently=True)

        return HttpResponse()

class RemoveFromWatchlistView(View):
    #removes a movie from the user's watchlist.
    def get(self, request, movie_id):
        MovieToWatch.objects.get(username=request.user, movie_id= Movie.objects.get(id=movie_id)).delete()
        messages.success(request, "The movie is removed from your watchlist!", fail_silently=True)

        return HttpResponse()
