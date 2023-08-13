from django import forms

from books.models import ReviewModel


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = (
            'review',
        )
        widgets = {
            'review': forms.Textarea(attrs={'rows': 10,
                                            'class': 'textarea'}),
        }