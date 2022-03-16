from django.test import TestCase, Client, override_settings
from moovie.forms import UserProfileForm
from moovie.models import *
from django.shortcuts import reverse
from decimal import *
from http import HTTPStatus
import datetime
from django.test.client import RequestFactory
from .views import AddToWatchlistView, RemoveFromWatchlistView
import tempfile, base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class MovieTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.movie = Movie.objects.create(title="The Lord of The Rings", duration=192, release_date=datetime.datetime(2001, 11, 16), average_rating=Decimal(5.00))

        self.director = Person.objects.create(name='Peter', surname='Jackson', person_type='Director')
        DirectorMovie.objects.create(movie_id=self.movie, person_id=self.director)

        self.actor = Person.objects.create(name='Orlando', surname='Bloom', person_type='Actor')
        ActorMovie.objects.create(movie_id=self.movie, person_id=self.actor)

        self.genre = Genre.objects.create(name='Fantastic')
        MovieGenre.objects.create(movie_id=self.movie, genre_name=self.genre)

        self.user = User.objects.create(username='test_user', password="3654789")
        UserProfile.objects.create(user=self.user)

        Review.objects.create(username=self.user, movie_id=self.movie, rating=Decimal(5.00))

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

    def test_if_rating_calculation_is_correct_after_editing(self):
        response = self.client.post(reverse('moovie:add_review', kwargs={'movie_id': 1}), {'username': 'test_user', 'comment':'random comment', 'header': 'random header', 'rating': Decimal(4.00)})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(1, Review.objects.filter(movie_id=1).count())
        self.assertEqual(Decimal(4.00), Movie.objects.get(id=1).average_rating)

    def test_if_movie_added_to_watchlist_correctly(self):
        request = self.factory.get(reverse('moovie:add_to_watchlist', kwargs={'movie_id': 1}))
        request.user = self.user
        response = AddToWatchlistView().get(request, 1)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(1, MovieToWatch.objects.filter(movie_id=1).count())
        self.assertEqual(1, MovieToWatch.objects.get(id=1).movie_id.id)

    def test_if_movie_removed_from_watchlist_correctly(self):
        MovieToWatch.objects.create(username=self.user, movie_id=self.movie)
        request = self.factory.get(reverse('moovie:remove_from_watchlist', kwargs={'movie_id': 1}))
        request.user = self.user
        response = RemoveFromWatchlistView().get(request, 1)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(0, MovieToWatch.objects.filter(movie_id=1).count())

class ContactMessageTests(TestCase):
    def test_if_data_is_stored_in_database_correctly(self):
        response = self.client.post(reverse('moovie:contact_us'), {'sender_name': 'cagdas', 'sender_email':'cagdas@email.com', 'subject': 'good app', 'message': 'you rock!'})
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(1, ContactMessage.objects.filter().count())
        self.assertEqual('cagdas', ContactMessage.objects.get(id=1).sender_name)
        self.assertEqual('cagdas@email.com', ContactMessage.objects.get(id=1).sender_email)
        self.assertEqual('good app', ContactMessage.objects.get(id=1).subject)
        self.assertEqual('you rock!', ContactMessage.objects.get(id=1).message)

class UserProfileTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testy_mctestface')
        self.user.set_password('testtesttest')
        self.user.save()
        self.userprofile = UserProfile.objects.create(user=self.user)
        self.movie1 = Movie.objects.create(title="The Lord of The Rings", duration=192, release_date=datetime.datetime(2001, 11, 16), average_rating=Decimal(5.00))
        self.movie2 = Movie.objects.create(title="Babe: Sheep Pig", duration=123, release_date=datetime.datetime(2004, 7, 12), average_rating=Decimal(4.70))
        
    def test_user_profile_returns_empty_on_init(self):
        response = self.client.get(reverse('moovie:show_user_profile', kwargs={'username': 'testy_mctestface'}))
        self.assertEqual(response.context['reviews_with_movies'], [])
        self.assertEqual(response.context['wishlist'], [])
        self.assertContains(response, "No reviews yet")
        self.assertContains(response, "Wishlist is empty")

    def test_user_profile_shows_added_reviews(self):
        self.review1 = Review.objects.create(username=self.user, movie_id=self.movie1, rating=Decimal(5.00))
        self.review2 = Review.objects.create(username=self.user, movie_id=self.movie2, rating=Decimal(5.00))
        response = self.client.get(reverse('moovie:show_user_profile', kwargs={'username': 'testy_mctestface'}))
        self.assertEqual(response.context['reviews_with_movies'], [{'review':self.review1, 'movie':self.movie1},{'review':self.review2, 'movie':self.movie2}])

    def test_user_profile_shows_items_added_to_wishlist(self):
        request = self.factory.get(reverse('moovie:add_to_watchlist', kwargs={'movie_id': 1}))
        request.user = self.user
        AddToWatchlistView().get(request, 1)
        request = self.factory.get(reverse('moovie:add_to_watchlist', kwargs={'movie_id': 2}))
        request.user = self.user
        AddToWatchlistView().get(request, 2)
        response = self.client.get(reverse('moovie:show_user_profile', kwargs={'username': 'testy_mctestface'}))
        self.assertEqual(response.context['wishlist'], [self.movie1, self.movie2])

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testy_mctestface', password='testtesttest')
        self.assertTrue(logged_in)

    def test_edit_profile_age(self):
        c = Client()
        logged_in = c.login(username='testy_mctestface', password='testtesttest')
        self.assertTrue(logged_in)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        response = c.post(reverse('moovie:edit_profile'), {'age': 666, 'picture':image, 'bio':'I like moovies'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserProfile.objects.get(user=self.user).age, 666)
        
    def test_edit_profile_bio(self):
        c = Client()
        logged_in = c.login(username='testy_mctestface', password='testtesttest')
        self.assertTrue(logged_in)

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        biography = 'I like mo0o0o0ovies'

        response = c.post(reverse('moovie:edit_profile'), {'age': 666, 'picture':image, 'bio':biography})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserProfile.objects.get(user=self.user).bio, biography)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())      # override settings for media dir to avoid filling up your disk
    def test_edit_profile_image(self):
        # image def for testing upload
        TEST_IMAGE = '''
        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
        '''.strip()
        
        c = Client()
        logged_in = c.login(username='testy_mctestface', password='testtesttest')
        self.assertTrue(logged_in)

        filename_string = 'special-temporary-file-with-distinctive-name'

        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)), 
            field_name='tempfile',
            name=filename_string+'.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )

        response = c.post(reverse('moovie:edit_profile'), {'age': 666, 'picture':image, 'bio':'hi'}, format='multipart')
        self.assertIn(filename_string, UserProfile.objects.get(user=self.user).picture.name)

    def test_updated_bio_displays(self):
        c = Client()
        logged_in = c.login(username='testy_mctestface', password='testtesttest')
        self.assertTrue(logged_in)

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        biography = 'I like mo0o0o0ovies'

        response = c.post(reverse('moovie:edit_profile'), {'age': 666, 'picture':image, 'bio':biography})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserProfile.objects.get(user=self.user).bio, biography)

        response = self.client.get(reverse('moovie:show_user_profile', kwargs={'username': 'testy_mctestface'}))
        self.assertEqual(biography,response.context['user_profile'].bio)

