from django import forms
from django.contrib.auth.models import User
from moovie.models import Review, ContactMessage, UserProfile


class ReviewForm(forms.ModelForm):
    header = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'full-size-text-input', 'placeholder': "Please enter a header."}),
        max_length=Review.HEADER_MAX_LENGTH, help_text="Header")
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'text-area', 'placeholder': "Please write your comment."}),
        max_length=Review.COMMENT_MAX_LENGTH, help_text="Comment")
    rating = forms.IntegerField(max_value=5, min_value=1, initial=1, help_text="Rating")

    class Meta:
        model = Review
        fields = ('header', 'comment', 'rating',)


class ContactMessageForm(forms.ModelForm):
    sender_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'half-size-text-input', 'placeholder': "Please enter your name."}),
        max_length=ContactMessage.NAME_MAX_LENGTH, help_text="Full Name")
    sender_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'half-size-text-input', 'placeholder': "Please enter your email."}),
        max_length=ContactMessage.EMAIL_MAX_LENGTH, help_text="Email")
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'full-size-text-input', 'placeholder': "Please enter a subject."}),
        max_length=ContactMessage.SUBJECT_MAX_LENGTH, help_text="Subject")
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'text-area', 'placeholder': "Please enter your message."}),
        max_length=ContactMessage.MESSAGE_MAX_LENGTH)

    class Meta:
        model = ContactMessage
        exclude = ('date',)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)