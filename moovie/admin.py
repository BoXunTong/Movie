from django.contrib import admin
from moovie.models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration', 'release_date', 'description', 'average_rating', 'image', 'create_date')

admin.site.register(Movie, MovieAdmin)
