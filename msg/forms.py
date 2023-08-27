from django import forms

from msg.models import MsgModel


class MessageForm(forms.ModelForm):
    class Meta:
        model = MsgModel
        fields = (
            'message',
        )
        widgets = {
            'message': forms.TextInput(attrs={
                'placeholder': 'Сообщение',
                'class': 'input-text'
            }),
        }