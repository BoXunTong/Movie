from django.contrib import admin
from moovie.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'bio', 'picture')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'average_rating', 'create_date')


class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'genre_name')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'person_type')


class ActorMovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'person_id')


class DirectorMovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'person_id')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie_id", "username", "header", "rating", "date")


class MovieToWatchAdmin(admin.ModelAdmin):
    list_display = ('username', 'movie_id')


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_email', 'sender_name', 'subject', 'message', 'date')


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieGenre, MovieGenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(ActorMovie, ActorMovieAdmin)
admin.site.register(DirectorMovie, DirectorMovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(MovieToWatch, MovieToWatchAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Genre, GenreAdmin)
