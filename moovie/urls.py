from unicodedata import name
from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [
    path('', views.index,name='index'),
    path('about/',views.about_us,name='about'),
    path('contact/',views.contact_us,name='contact'),
    path('movie/<slug:movie_id>/',views.show_movie_profile,name='movie_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('search_result/',views.show_search_result,name='search_result'),
    path('user_profile/',views.show_user_profile,name='user_profile'),
]
