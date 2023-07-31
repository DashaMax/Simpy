from django import forms

from quotes.models import QuoteModel


class AddQuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteModel
        fields = (
            'text',
        )
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10,
                                          'class': 'textarea'}),
        }


class UserAddQuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteModel
        fields = (
            'book',
            'text',
        )
        labels = {
            'book': 'Книга',
            'text': 'Цитата',
        }

    def __init__(self, *args, **kwargs):
        super(UserAddQuoteForm, self).__init__(*args, **kwargs)
        self.fields['book'].empty_label = 'Выберите книгу:'

        for title, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-field'})