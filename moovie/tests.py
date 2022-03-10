from django.test import TestCase
from moovie.models import *
from django.shortcuts import reverse
from decimal import *
from http import HTTPStatus
import datetime

class MovieTests(TestCase):
    def setUp(self):
        movie = Movie.objects.create(title="The Lord of The Rings", duration=192, release_date=datetime.datetime(2001, 11, 16), average_rating=Decimal(5.00))

        director = Person.objects.create(name='Peter', surname='Jackson', person_type='Director')
        DirectorMovie.objects.create(movie_id=movie, person_id=director)

        actor = Person.objects.create(name='Orlando', surname='Bloom', person_type='Actor')
        ActorMovie.objects.create(movie_id=movie, person_id=actor)

        genre = Genre.objects.create(name='Fantastic')
        MovieGenre.objects.create(movie_id=movie, genre_name=genre)

        user = User.objects.create(username='test_user')
        UserProfile.objects.create(user=user)

        Review.objects.create(username=user, movie_id=movie, rating=Decimal(5.00))

    def test_if_show_movie_retrieves_correct_info_when_all_data_exists(self):
        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("The Lord of The Rings", response.context['movie'].title)
        self.assertEqual("Peter", response.context['directors'][0].name)
        self.assertEqual("Orlando", response.context['stars'][0].name)
        self.assertEqual("Fantastic", response.context['genres'][0].name)
        self.assertEqual("test_user", response.context['reviews_with_user_info'][0]['user'].user.username)

    def test_if_show_movie_returns_None_info_when_there_is_no_movie(self):
        Movie.objects.filter(title='The Lord of The Rings').delete()

        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsNone(response.context['movie'])
        self.assertIsNone(response.context['directors'])
        self.assertIsNone(response.context['stars'])
        self.assertIsNone(response.context['genres'])
        self.assertIsNone(response.context['reviews_with_user_info'])

    def test_if_show_movie_returns_empty_when_there_is_no_director(self):
        Person.objects.filter(name='Peter').delete()

        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("The Lord of The Rings", response.context['movie'].title)
        self.assertEqual([], response.context['directors'])
        self.assertEqual("Orlando", response.context['stars'][0].name)
        self.assertEqual("Fantastic", response.context['genres'][0].name)
        self.assertEqual("test_user", response.context['reviews_with_user_info'][0]['user'].user.username)

    def test_if_show_movie_returns_empty_when_there_is_no_actor(self):
        Person.objects.filter(name='Orlando').delete()

        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("The Lord of The Rings", response.context['movie'].title)
        self.assertEqual("Peter", response.context['directors'][0].name)
        self.assertEqual([], response.context['stars'])
        self.assertEqual("Fantastic", response.context['genres'][0].name)
        self.assertEqual("test_user", response.context['reviews_with_user_info'][0]['user'].user.username)
    
    def test_if_show_movie_returns_empty_when_there_is_no_genre(self):
        Genre.objects.filter(name='Fantastic').delete()

        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("The Lord of The Rings", response.context['movie'].title)
        self.assertEqual("Peter", response.context['directors'][0].name)
        self.assertEqual("Orlando", response.context['stars'][0].name)
        self.assertEqual([], response.context['genres'])
        self.assertEqual("test_user", response.context['reviews_with_user_info'][0]['user'].user.username)

    def test_if_show_movie_returns_empty_when_there_is_no_review(self):
        Review.objects.filter(movie_id=1).delete()

        response = self.client.get(reverse('moovie:show_movie_profile', kwargs={'movie_id': 1}), follow=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("The Lord of The Rings", response.context['movie'].title)
        self.assertEqual("Peter", response.context['directors'][0].name)
        self.assertEqual("Orlando", response.context['stars'][0].name)
        self.assertEqual("Fantastic", response.context['genres'][0].name)
        self.assertEqual([], response.context['reviews_with_user_info'])

    def test_if_rating_calculation_is_correct(self):
        response = self.client.post(reverse('moovie:add_review', kwargs={'movie_id': 1}), {'username': 'test_user', 'comment':'random comment', 'header': 'random header', 'rating': Decimal(4.00)})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(2, Review.objects.filter(movie_id=1).count())
        self.assertEqual(Decimal(4.50), Movie.objects.get(id=1).average_rating)

class ContactMessageTests(TestCase):
    def test_if_data_is_stored_in_database_correctly(self):
        response = self.client.post(reverse('moovie:contact_us'), {'sender_name': 'cagdas', 'sender_email':'cagdas@email.com', 'subject': 'good app', 'message': 'you rock!'})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(1, ContactMessage.objects.filter().count())
        self.assertEqual('cagdas', ContactMessage.objects.get(id=1).sender_name)
        self.assertEqual('cagdas@email.com', ContactMessage.objects.get(id=1).sender_email)
        self.assertEqual('good app', ContactMessage.objects.get(id=1).subject)
        self.assertEqual('you rock!', ContactMessage.objects.get(id=1).message)