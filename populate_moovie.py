import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITech_group_project.settings')

import django
django.setup()

from moovie.models import *
from django.core.files.images import ImageFile
from decimal import *
import datetime

def populate():
    add_movie('Harry Potter and the Philosophers Stone', 152, datetime.datetime(2001, 11, 16), 'First movie of the series.', Decimal(4.71), "movie_images/HarryPotter1.jpg")


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

def add_user_profile(username, password, email, first_name, last_name, age, image, bio):
    user = User.objects.get_or_create(username=username)[0]
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.set_password(password)
    user.save()

    user_profile = UserProfile.objects.create(user=user, age=age, image=image, bio=bio)
    user_profile.save()
    return user_profile

def add_review(username, movie_id, comment, header, rating, date):
    review = Review.objects.get_or_create(username=username, movie_id=movie_id)[0]
    review.comment = comment
    review.header = header
    review.rating = rating
    review.date = date
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