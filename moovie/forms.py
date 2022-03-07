from django import forms
from moovie.models import Review, ContactMessage


class ReviewForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter a header."}), max_length=Review.HEADER_MAX_LENGTH, help_text="Header")
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control md-textarea', 'placeholder': "Please write your comment."}), max_length=Review.COMMENT_MAX_LENGTH, help_text="Comment")
    rating = forms.IntegerField(max_value=5, min_value=1, initial=1, help_text="Rating")

    class Meta:
        model = Review
        fields = ('header', 'comment', 'rating',)

class ContactMessageForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your Name *"}), max_length=ContactMessage.NAME_MAX_LENGTH, help_text="Full Name")
    sender_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Your Email *"}), max_length=ContactMessage.EMAIL_MAX_LENGTH, help_text="Email")
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject *"}), max_length=ContactMessage.SUBJECT_MAX_LENGTH, help_text="Subject")
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control md-textarea', 'placeholder': "Type Your Message..."}), max_length=ContactMessage.MESSAGE_MAX_LENGTH)

    class Meta:
        model = ContactMessage
        exclude = ('date',)