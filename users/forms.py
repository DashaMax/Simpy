from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserChangeForm,
                                       UserCreationForm)

from blogs.models import BlogModel
from users.models import UserModel


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'input-field'
        })
    )

    class Meta:
        model = UserModel
        fields = (
            'username',
            'password'
        )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин',
            'class': 'input-field'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя',
            'class': 'input-field'
        })
    )
    email = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail',
            'class': 'input-field'
        })
    )
    password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'input-field'
        })
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'class': 'input-field'
        })
    )

    class Meta:
        model = UserModel
        fields = (
            'username',
            'first_name',
            'email',
            'password1',
            'password2'
        )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'Введите e-mail',
            'class': 'input-field'
        }),
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Введите новый пароль',
            'class': 'input-field'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Повторите пароль',
            'class': 'input-field'
        }),
    )


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
            'about',
            'is_send_notifications',
        )
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'input-field'
            }),
            'date_of_birth': forms.TextInput(attrs={
                'type': 'date',
                'class': 'input-field'
            }),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
            'sex': 'Пол',
            'city': 'Город',
            'date_of_birth': 'Дата рождения',
            'about': 'О себе',
            'is_send_notifications': 'Получать уведомления'
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Выберите город:'

        for title, field in self.fields.items():
            if title not in ('image', 'date_of_birth', 'is_send_notifications', 'password'):
                field.widget.attrs.update({'class': 'input-field'})


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = (
            'title',
            'image',
            'blog'
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field'
            }),
            'image': forms.FileInput(attrs={
                'class': 'input-field'
            }),
            'blog': forms.Textarea(attrs={
                'rows': 10, 'class': 'input-field'
            }),
        }
        labels = {
            'title': 'Название',
            'image': 'Фото',
            'blog': 'Текст',
        }