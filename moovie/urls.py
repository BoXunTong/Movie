from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('movie/<int:movie_id>/', views.show_movie_profile, name='show_movie_profile'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('user/<str:username>/', views.show_user_profile, name='show_user_profile'),
    path('contact/', views.contact_us, name='contact_us'),

]
