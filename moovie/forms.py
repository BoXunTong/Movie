from django import forms
from moovie.models import Review, ContactMessage


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(max_length=Review.COMMENT_MAX_LENGTH, help_text="Please enter a comment.")
    header = forms.CharField(max_length=Review.HEADER_MAX_LENGTH, help_text="Please enter a header.")
    rating = forms.IntegerField(max_value=5, min_value=1, initial=1)

    class Meta:
        model = Review
        fields = ('comment', 'header', 'rating',)

class ContactMessageForm(forms.ModelForm):
    sender_email = forms.EmailField(max_length=ContactMessage.EMAIL_MAX_LENGTH, help_text="Please enter your email.")
    sender_name = forms.CharField(max_length=ContactMessage.NAME_MAX_LENGTH, help_text="Please enter your name.")
    subject = forms.CharField(max_length=ContactMessage.SUBJECT_MAX_LENGTH, help_text="Please enter a subject.")
    message = forms.CharField(max_length=ContactMessage.MESSAGE_MAX_LENGTH, help_text="Please enter your message.")

    class Meta:
        model = ContactMessage
        exclude = ('date',)