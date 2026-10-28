from django import forms
from Review.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=Review.RATING_CHOICES)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

