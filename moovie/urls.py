from django.urls import path
from moovie import views

app_name = 'moovie'

urlpatterns = [
    path('', views.index, name='index'),
]
