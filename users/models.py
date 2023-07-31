from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify


class UserModel(AbstractUser):
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True, blank=True)
    sex = models.CharField(max_length=50, choices=settings.SEX, verbose_name='Пол')
    city = models.ForeignKey(to='CityModel', on_delete=models.CASCADE, verbose_name='Город', blank=True, null=True)
    image = models.ImageField(upload_to='user/%Y/%m/%d/', verbose_name='Фото', default='profile-account.png')
    #image = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото', default='profile-default.png')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    book = models.ManyToManyField('books.BookModel', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserModel, self).save(*args, **kwargs)


class CityModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']

    def __str__(self):
        return self.title
