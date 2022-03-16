from multiprocessing import context
from platform import release
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.shortcuts import render, redirect, reverse
from moovie.models import *
from moovie.forms import *
from django.http import HttpResponse
from django.contrib import messages

# Index view class
class IndexView(View):
    def get(self, request):
        context_dict = {}
        top_3_movie = Movie.objects.order_by('-average_rating')[0:3]
        movies_by_rating = Movie.objects.order_by('-average_rating')[3:9]
        movies_by_release = Movie.objects.order_by('-release_date')[:6]

        context_dict['top_3_movie'] = top_3_movie
        context_dict['movies_by_rating'] = movies_by_rating
        context_dict['movies_by_release'] = movies_by_release

        return render(request, 'moovie/index.html', context_dict)

class RegisterView(View):
    #shows the register page.
    def get (self, request):
        user_form = UserForm()

        return render(request, 'moovie/register.html', context={'user_form': user_form})

    #registers users.
    def post(self, request):
        user_form = UserForm(request.POST)

        #checks if the form is valid.
        if user_form.is_valid():
            #saves user
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #creates user profile associated with the user saved.
            UserProfile.objects.create(user=user)
            messages.success(request, "Congratulation! Welcome to Moovie!")
            return redirect(reverse('moovie:login'))
        else:
            messages.error(request, "Something went wrong, please try again later.")
            print(user_form.errors)

        return render(request, 'moovie/register.html', context={'user_form': user_form})

class LoginView(View):
    #shows the login page.
    def get (self, request):

        return render(request, 'moovie/login.html')

    #logs the user in.
    def post(self, request):
        #gets user info from the request.
        username = request.POST['username']
        password = request.POST['password']

        #authenticates the user.
        user = authenticate(username=username, password=password)

        if user:
            #checks if the user is active.
            if user.is_active:
                #logs the user in.
                login(request, user)
                return redirect(reverse('moovie:index'))
            else:
                messages.error(request, 'The user is not active.')
                return redirect(reverse('moovie:login'))
        else:
            messages.error(request, "Something went wrong, please try again later.")
            return redirect(reverse('moovie:login'))

@login_required
def user_logout(request):
    #logs the user out.
    logout(request)

    messages.success(request, "You logged out!")
    return redirect(reverse('moovie:index'))

# Search result view class
class searchResultView(View):
    # (get) direct access to the search result page
    def get(self, request):
        context_dict = {}
        if request.method == 'get':
            # maintain current page
            query = None
        return render(request, 'moovie/search_result.html', context=context_dict)

    # (post) must enter request to access
    def post(self, request):
        context_dict = {}
        if request.method == 'POST':
            query = request.POST['query'].strip()
            # get query from base
            keyword = request.POST['search_dropdown']
            # get category from base
            if keyword == 'Title':
                keyword = 1
            elif keyword == 'Director':
                keyword = 2
            elif keyword == 'Actor':
                keyword = 3
            else:
                keyword = 4
            if query:
                context_dict['result_list'] = self.run_query(query, keyword)
                context_dict['query'] = query
        return render(request, 'moovie/search_result.html', context=context_dict)
    # if query = actor & director with their surname or name
    def get_movie_from_person(self, search_terms, keyword):
        person_list_name = []
        person_list_surname = []
        movie_list = []
        if search_terms:
            # filter the query within the Person database
            person_list_name = Person.objects.filter(name__icontains=search_terms)
            person_list_surname = Person.objects.filter(surname__icontains=search_terms)
        for person_name in person_list_name:
            if keyword == 2:
                # match the name with data in director object database
                directors = DirectorMovie.objects.filter(person_id=person_name)
                for director in directors:
                    movie_id = director.movie_id.id
                    # get movie model
                    movie_list.append(Movie.objects.get(id=movie_id))
            elif keyword == 3:
                actors = ActorMovie.objects.filter(person_id=person_name)
                for actor in actors:
                    movie_id = actor.movie_id.id
                    movie_list.append(Movie.objects.get(id=movie_id))

        for person_surname in person_list_surname:
            if keyword == 2:
                # match the name with data in director object database
                directors = DirectorMovie.objects.filter(person_id=person_surname)
                for director in directors:
                    movie_id = director.movie_id.id
                    # get movie model
                    movie_list.append(Movie.objects.get(id=movie_id))
            elif keyword == 3:
                actors = ActorMovie.objects.filter(person_id=person_surname)
                print(actors)
                for actor in actors:
                    movie_id = actor.movie_id.id
                    movie_list.append(Movie.objects.get(id=movie_id))
        # combine with set function
        movie_list = set(movie_list)
        return movie_list
    # get move directly from Movie object
    def get_movie_list(self, search_terms):
        movie_list = []
        if search_terms:
            movie_list = Movie.objects.filter(title__icontains=search_terms)
        return movie_list

    # get move directly from Genre object
    def get_movie_from_genre(self, search_terms):
        movie_list = []
        print(search_terms)
        if search_terms:
            movie_genre_list = MovieGenre.objects.filter(genre_name=search_terms)
        for movie_genre in movie_genre_list:
            movie_list.append(movie_genre.movie_id)
        return movie_list

    def run_query(self, search_terms, keyword):
        search_results = []
        if (keyword == 1):
            search_results = self.get_movie_list(search_terms)
        elif(keyword == 2| keyword == 3):
            search_results = self.get_movie_from_person(search_terms, keyword)
        else:
            search_results = self.get_movie_from_genre(search_terms)
        results = []

        for result in search_results:
            movie_view = MovieView()
            # modify data formats for output
            # modify director
            director = movie_view.get_directors_for_movie(result)
            director = str(director)
            director = director.split('-', 1)
            director = director[1].split('>', 1)
            director = director[0]

            # modify genre
            genre = movie_view.get_genres_for_movie(result)
            genre = str(genre)
            genre = genre.split(':', 1)
            genre = genre[1].split('>', 1)
            genre = genre[0]
            
            # modify release_date
            release_date = str(result.release_date)
            release_date = release_date.split(' ', 1)
            release_date = release_date[0]
            
            # return the set of result
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
        # call the runqery from searchResult view
        context_dict['result_list'] = searchResultView.run_query(query, keyword)
        context_dict['query'] = query 
    return render(request, 'moovie/search_result.html', context=context_dict)


def show_user_profile(request, username):
    context_dict = {}
    try:
        # get the User and UserProfile objects for this user
        thisuser = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=thisuser.id)
        context_dict['user_profile'] = user_profile

        # get all reviews (and associated Movie objects) authored by this user
        reviews_with_movies = get_reviews_for_user(thisuser)
        context_dict['reviews_with_movies'] = reviews_with_movies

        # get the Movie objects in this user's wishlist
        wishlist = get_wishlist_for_user(thisuser)
        context_dict['wishlist'] = wishlist

    except (User.DoesNotExist, UserProfile.DoesNotExist):
        # if there is no user with this username, return empty fields
        context_dict['user'] = None
        context_dict['user_profile'] = None
        context_dict['reviews_with_movies'] = None
        context_dict['wishlist'] = None

    return render(request, 'moovie/user_profile.html', context = context_dict)

def get_reviews_for_user(user):
    # takes a User objects and returns all Reviews authored by that User
    reviews = Review.objects.filter(username=user)
    reviews_with_movies = []
    for review in reviews:
        movie_id = review.movie_id
        reviews_with_movies.append({'review':review, 'movie':movie_id})
    return reviews_with_movies

def get_wishlist_for_user(user):
    # takes a User objects and returns all Movies in that User's wishlist
    movies_to_watch = MovieToWatch.objects.filter(username=user)
    wishlist = []
    for mov2w in movies_to_watch:
        wishlist.append(mov2w.movie_id)
    return wishlist

# About us view class
class AboutUsView(View):
    def get(self, request):
        return render(request, 'moovie/about.html', context={})

@login_required
def edit_profile(request):

    # the edit profile function is only available to logged in users
    # they can also only edit their own profile!!

    # get the logged in user; retreive their UserProfile object; load this into a form
    curr_user = request.user
    curr_user_profile = UserProfile.objects.get(user=curr_user.id)
    form = UserProfileForm(instance=curr_user_profile)

    # parse submitted form data
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=curr_user_profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!", fail_silently=True)
            return redirect(reverse('moovie:edit_profile'))
        else:
            messages.error(request, "Something went wrong with the from!", fail_silently=True)
            print(form.errors)

    return render(request, 'moovie/edit_profile.html', {'form': form})


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

    # saves a new movie directly into the database.
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
