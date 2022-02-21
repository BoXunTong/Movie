from django.shortcuts import render

def index(request):
    return render(request, 'moovie/index.html', context={})

def contact_us(request):
    return render(request, 'moovie/contact.html', context = {})

def show_movie_profile(request):
    return render(request, 'moovie/movie_profile.html', context = {})

def show_search_result(request):
    return render(request, 'moovie/search_result.html', context = {})

def show_user_profile(request):
    # this is the publicly visible profile of any user
    return render(request, 'moovie/user_profile.html', context = {})

def about_us(request):
    return render(request, 'moovie/about.html', context = {})

def user_login(request):
    return render(request, 'moovie/login.html', context = {})

def user_signup(request):
    return render(request, 'moovie/signup.html', context = {})

# @login_required
def edit_profile(request):
    # this is the profile of the logged in user (with edit functionality)
    return render(request, 'moovie/edit_profile.html', context = {})



