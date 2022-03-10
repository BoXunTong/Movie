from unicodedata import name
from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('search_result/', views.show_search_result, name='show_search_result'),
    path('movie/<int:movie_id>/', views.show_movie_profile, name='show_movie_profile'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('contact/', views.contact_us, name='contact_us'),
    path('add-to-watchlist/', views.AddToWatchlistView.as_view(), name='add_to_watchlist'),
    path('remove-from-watchlist/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout')
]
