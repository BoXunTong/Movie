from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.show_movie_profile, name='show_movie_profile'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('contact/', views.contact_us, name='contact_us'),
]
