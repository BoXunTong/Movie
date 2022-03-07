from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('movie/<slug:movie_id>/', views.show_movie_profile, name='show_movie_profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

]
