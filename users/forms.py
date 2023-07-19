from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import UserModel


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Логин',
        'class': 'input-field'
    }))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
        'class': 'input-field'
    }))

    class Meta:
        model = UserModel
        fields = (
            'username',
            'password'
        )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Логин',
        'class': 'input-field'
    }))
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
        'class': 'input-field'
    }))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Фамилия',
        'class': 'input-field'
    }))
    email = forms.CharField(max_length=150, required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail',
        'class': 'input-field'
    }))
    # image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
    #     'class': 'input-field'
    # }))
    # date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={
    #     'type': 'date',
    #     'placeholder': 'E-mail',
    #     'class': 'input-field'
    # }))
    # about = forms.CharField(required=False, widget=forms.Textarea(attrs={
    #     'placeholder': 'О себе',
    #     'class': 'input-field'
    # }))
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
        'class': 'input-field'
    }))
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль',
        'class': 'input-field'
    }))

    class Meta:
        model = UserModel
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'sex',
            # 'city',
            # 'image',
            # 'date_of_birth',
            # 'about',
            'password1',
            'password2'
        )
