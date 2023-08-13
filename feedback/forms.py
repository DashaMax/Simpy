from django import forms

from feedback.models import FeedbackModel


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = (
            'title',
            'email',
            'feedback'
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Тема обращения',
                'class': 'input-field'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ваша почта для связи',
                'class': 'input-field'
            }),
            'feedback': forms.Textarea(attrs={
                'placeholder': 'Сообщение',
                'class': 'input-field'
            })
        }