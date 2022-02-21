from django.shortcuts import render

def index(request):
    return render(request, 'moovie/index.html', context={})
