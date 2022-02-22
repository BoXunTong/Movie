from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<slug:movie_id>/', views.show_movie_profile, name='show_movie_profile'),
]
