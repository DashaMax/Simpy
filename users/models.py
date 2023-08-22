from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify


class UserModel(AbstractUser):
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True, blank=True)
    email = models.EmailField(max_length=150, unique=True, verbose_name='E-mail')
    sex = models.CharField(max_length=50, choices=settings.SEX, verbose_name='Пол')
    city = models.ForeignKey(to='CityModel', on_delete=models.CASCADE, verbose_name='Город', blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото', default='profile-default.jpg')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    book = models.ManyToManyField('books.BookModel', blank=True)
    is_send_notifications = models.BooleanField(verbose_name='Отправлять уведомления в телеграм', default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'username',
        )


class CityModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = (
            'title',
        )