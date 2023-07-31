from django import forms

from comments.models import CommentModel


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = (
            'comment',
        )
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
        }