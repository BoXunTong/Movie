import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITech_group_project.settings')

import django
django.setup()

from moovie.models import *
from django.core.files.images import ImageFile
from decimal import *
import datetime


def populate():
    # Add user test
    user1 = add_user('user1', '12345678', 'example@gmail.com', 'Rogers', 'Choi')
    user2 = add_user('user2', '87654321', 'example@gmail.com', 'Anne', 'Hathaway')
    add_user_profile(user1, 25, 'profile_images/user1.jpg', 'my bio')
    add_user_profile(user2, 25, 'profile_images/user1.jpg', '2 bio')

    # Movie and actors test
    movie1 = add_movie('Harry Potter and the Philosophers Stone', 152, datetime.datetime(2001, 11, 16), 'First movie of the series.', Decimal(4.71), "movie_images/HarryPotter1.jpg")
    person = add_person("Daniel", 'Radcliffe', 'person_images/Daniel_Radcliffe.jpg', 'Actor')
    person2 = add_person("Emma", "Watson", 'person_images/Emma_Watson.jpg', 'Actor')
    person3 = add_person('Chris', 'Columbus', 'person_images/Chris_Columbus.jpg', 'Director')
    add_actor_movie(movie1, person)
    add_actor_movie(movie1, person2)
    add_director_movie(movie1, person3)

    movie2 = add_movie('Harry Potter and the Prisoner of Azkaban', 142, datetime.datetime(2004, 6, 4), 'Some description', Decimal(4.56), 'movie_images/HarryPotter3.jpg')
    person4 = add_person('Alfonso', 'Cuarón', 'person_images/Alfonso_Cuarón.jpg', 'Director')
    add_actor_movie(movie2, person)
    add_actor_movie(movie2, person2)
    add_director_movie(movie2, person4)

    # user review test
    add_review(user1, movie1, 'comment test', 'header test', Decimal(4.2))

    # Movie to watch test
    add_movie_to_watch(user1, movie1)
    add_movie_to_watch(user2, movie1)

    # MovieGenre test
    adventure = add_genre('Adventure')
    fantasy = add_genre('Fantasy')
    add_movie_genre(movie1, adventure)
    add_movie_genre(movie1, fantasy)
    add_movie_genre(movie2, adventure)
    add_movie_genre(movie2, fantasy)

    # Contact message test
    add_contact_message('example@gmail.com', 'Anonymous', 'test', 'test', datetime.datetime)



def add_movie(title, duration, release_date, description, average_rating, image):
    movie = Movie.objects.get_or_create(title=title, duration=duration, release_date=release_date)[0]
    movie.description = description
    movie.average_rating = average_rating
    movie.image = image
    movie.save()
    return movie

def add_genre(name):
    genre = Genre.objects.get_or_create(name=name)[0]
    genre.save()
    return genre

def add_person(name, surname, image, person_type):
    person = Person.objects.create(name=name, surname=surname, image=image, person_type=person_type)
    person.save()
    return person

def add_director_movie(movie_id, person_id):
    director_movie = DirectorMovie.objects.get_or_create(movie_id=movie_id, person_id=person_id)[0]
    director_movie.save()
    return director_movie

def add_actor_movie(movie_id, person_id):
    actor_movie = ActorMovie.objects.get_or_create(movie_id=movie_id, person_id=person_id)[0]
    actor_movie.save()
    return actor_movie


def add_user(username, password, email, first_name, last_name):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(password)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def add_user_profile(user, age, picture, bio):
    user_profile = UserProfile.objects.get_or_create(user=user, age=age, picture=picture, bio=bio)
    return user_profile


def add_review(username, movie_id, comment, header, rating):
    review = Review.objects.get_or_create(username=username, movie_id=movie_id)[0]
    review.comment = comment
    review.header = header
    review.rating = rating
    review.save()
    return review


def add_movie_to_watch(username, movie_id):
    movie_to_watch = MovieToWatch.objects.get_or_create(username=username, movie_id=movie_id)[0]
    movie_to_watch.save()
    return movie_to_watch

def add_movie_genre(movie_id, genre_name):
    movie_genre = MovieGenre.objects.get_or_create(movie_id=movie_id, genre_name=genre_name)[0]
    movie_genre.save()
    return movie_genre

def add_contact_message(sender_email, sender_name, subject, message, date):
    contact_message = ContactMessage.objects.create(sender_email=sender_email, sender_name=sender_name, subject=subject, message=message, date=date)
    contact_message.save()
    return contact_message

if __name__ == '__main__':
    print('Starting Moovie population script...')
    populate()