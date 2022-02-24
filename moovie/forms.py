from django import forms
from moovie.models import Review


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(max_length=Review.COMMENT_MAX_LENGTH, help_text="Please enter a comment.")
    header = forms.CharField(max_length=Review.HEADER_MAX_LENGTH, help_text="Please enter a header.")
    rating = forms.IntegerField(initial=0)

    class Meta:
        model = Review
        fields = ('comment', 'header', 'rating',)