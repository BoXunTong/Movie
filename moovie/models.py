from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.TextField(max_length=128, blank=False, unique=True)
    duration = models.IntegerField(default=0)
    release_date = models.DateTimeField(blank=False)
    description = models.TextField(max_length=256)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='movie_images', default='movie_images/placeholder.png')
    poster = models.ImageField(upload_to='poster_images', default='poster_images/placeholder.png')
    create_date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.id) + '-' + self.title


class Genre(models.Model):
    name = models.CharField(max_length=32, primary_key=True, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=64, blank=False)
    surname = models.CharField(max_length=32, blank=False)
    image = models.ImageField(upload_to='person_images', default='person_images/placeholder.jpg')
    person_type = models.CharField(max_length=16, blank=False)

    def __str__(self):
        return str(self.id) + '-' + self.name + ' ' + self.surname


class DirectorMovie(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)


class ActorMovie(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)


class UserProfile(models.Model):
    BIO_MAX_LENGTH = 128

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField(default=0)
    bio = models.TextField(max_length=BIO_MAX_LENGTH, blank=True)
    picture = models.ImageField(upload_to='profile_images', default='profile_images/placeholder.jpg')

    def __str__(self):
        return self.user.username


class Review(models.Model):
    COMMENT_MAX_LENGTH = 512
    HEADER_MAX_LENGTH = 128

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)

    comment = models.TextField(max_length=COMMENT_MAX_LENGTH)
    header = models.TextField(max_length=HEADER_MAX_LENGTH)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.header


class MovieToWatch(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


class MovieGenre(models.Model):
    genre_name = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


class ContactMessage(models.Model):
    EMAIL_MAX_LENGTH = 64
    NAME_MAX_LENGTH = 64
    SUBJECT_MAX_LENGTH = 128
    MESSAGE_MAX_LENGTH = 512

    sender_email = models.CharField(max_length=EMAIL_MAX_LENGTH, blank=False)
    sender_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=False)
    subject = models.TextField(max_length=SUBJECT_MAX_LENGTH, blank=False)
    message = models.TextField(max_length=MESSAGE_MAX_LENGTH, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.subject
