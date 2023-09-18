from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify


class UserModel(AbstractUser):
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True, blank=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    email = models.EmailField(max_length=150, unique=True, verbose_name='E-mail')
    sex = models.CharField(max_length=50, choices=settings.SEX, verbose_name='Пол', blank=True, null=True)
    city = models.ForeignKey(to='CityModel', on_delete=models.CASCADE, verbose_name='Город', blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото', default='profile-default.jpg')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    book = models.ManyToManyField('books.BookModel', blank=True)
    is_send_notifications = models.BooleanField(verbose_name='Отправлять уведомления в телеграм', default=False)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name)
        super(UserModel, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width > 300:
            size = (300, int(img.height / img.width * 300))
            img.thumbnail(size)
            img.save(self.image.path)

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