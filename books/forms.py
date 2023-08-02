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


class FeedbackForm(forms.Form):
    title = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Тема обращения',
        'class': 'input-field'
    }))
    email = forms.CharField(max_length=150, widget=forms.EmailInput(attrs={
        'placeholder': 'Ваша почта для связи',
        'class': 'input-field'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Сообщение',
        'class': 'input-field'
    }))