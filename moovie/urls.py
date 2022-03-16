from unicodedata import name
from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('search_result/', views.SearchResultView.as_view(), name='show_search_result'),
    path('search-tag/<str:search_type>/<str:query>', views.SearchTagView.as_view(), name='search_tag'),
    path('movie/<int:movie_id>/', views.MovieView.as_view(), name='show_movie_profile'),
    path('movie/<int:movie_id>/review/', views.ReviewView.as_view(), name='add_review'),
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),
    path('add-movie/', views.AddMovieView.as_view(), name='add_movie'),
    path('add-to-watchlist/<int:movie_id>/', views.AddToWatchlistView.as_view(), name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<str:username>/', views.show_user_profile, name='show_user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
