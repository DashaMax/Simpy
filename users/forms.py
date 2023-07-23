from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
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
        # widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'input-field'}),
        #     'password': forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'input-field'}),
        # }


class UserRegisterForm(UserCreationForm):
    # username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
    #     'placeholder': 'Логин',
    #     'class': 'input-field'
    # }))
    # first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
    #     'placeholder': 'Имя',
    #     'class': 'input-field'
    # }))
    # last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
    #     'placeholder': 'Фамилия',
    #     'class': 'input-field'
    # }))
    # email = forms.CharField(max_length=150, required=False, widget=forms.EmailInput(attrs={
    #     'placeholder': 'E-mail',
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
            'password1',
            'password2'
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'input-field'}),
            'sex': forms.Select(attrs={'class': 'input-field'}),
            # 'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'input-field'}),
            # 'password2': forms.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class': 'input-field'}),
        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'sex',
            'city',
            'image',
            'date_of_birth',
            'about'
        )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'input-field'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
            'sex': 'Пол',
            'city': 'Город',
            'date_of_birth': 'Дата рождения',
            'about': 'О себе'
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Выберите город:'

        for title, field in self.fields.items():
            if field not in ('image', 'date_of_birth'):
                field.widget.attrs.update({'class': 'input-field'})