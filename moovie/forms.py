from django import forms
from django.contrib.auth.models import User
from moovie.models import Review, ContactMessage, UserProfile, Movie, Person, Genre

class ReviewForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter a header."}), max_length=Review.HEADER_MAX_LENGTH, help_text="Header")
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control md-textarea', 'placeholder': "Please write your comment."}), max_length=Review.COMMENT_MAX_LENGTH, help_text="Comment")
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'class':'custom-range', 'min':'0', 'max':'5'}), help_text="Rating")

    class Meta:
        model = Review
        fields = ('header', 'rating', 'comment',)


class ContactMessageForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your Name *"}),
                                  max_length=ContactMessage.NAME_MAX_LENGTH, help_text="Full Name")
    sender_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Your Email *"}),
        max_length=ContactMessage.EMAIL_MAX_LENGTH, help_text="Email")
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject *"}),
                              max_length=ContactMessage.SUBJECT_MAX_LENGTH, help_text="Subject")
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control md-textarea', 'placeholder': "Type Your Message..."}),
        max_length=ContactMessage.MESSAGE_MAX_LENGTH)

    class Meta:
        model = ContactMessage
        exclude = ('date',)

class AddMovieForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Title *"}),
                                    max_length=Movie.TITLE_MAX_LENGTH, help_text="Title")
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Duration - in minutes *"}), 
                                    help_text="Duration")
    release_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': "Release Date - yyyy-mm-dd *"}),
                                    help_text="Release Date")
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Description *"}),
                                    max_length=Movie.DESCRIPTION_MAX_LENGTH, help_text="Description")
    image = forms.ImageField(widget=forms.ClearableFileInput(), help_text="Movie Image")
    poster = forms.ImageField(widget=forms.ClearableFileInput(), help_text="Movie Poster")

    class Meta:
        model = Movie
        exclude = ('average_rating', 'create_date')

class AddDirectorForm(forms.ModelForm):
    director_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Director Name (if multiple, separate with a comma) *"}),
                                    max_length=Person.NAME_MAX_LENGTH, help_text="Director Name")
    director_surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Director Surname (if multiple, separate with a comma) *"}),
                                    max_length=Person.SURNAME_MAX_LENGTH, help_text="Director Surname")
    class Meta:
        model = Person
        fields = ('director_name', 'director_surname',)

class AddActorForm(forms.ModelForm):
    actor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Actor Name (if multiple, separate with a comma) *"}),
                                    max_length=Person.NAME_MAX_LENGTH, help_text="Actor Name")
    actor_surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Actor Surname (if multiple, separate with a comma) *"}),
                                    max_length=Person.SURNAME_MAX_LENGTH, help_text="Actor Surname")
    class Meta:
        model = Person
        fields = ('actor_name', 'actor_surname',)

class AddGenreForm(forms.ModelForm):
    genre_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Genre (if multiple, separate with a comma) *"}),
                                    max_length=Genre.NAME_MAX_LENGTH, help_text="Genre")
    class Meta:
        model = Genre
        fields = ('genre_name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Age *"}), help_text="Age")
    picture = forms.ImageField(widget=forms.ClearableFileInput(), help_text="Profile Image")
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Bio *"}), max_length=UserProfile.BIO_MAX_LENGTH, help_text="Bio")
    
    class Meta:
        model = UserProfile
        fields = ('age', 'picture', 'bio')
