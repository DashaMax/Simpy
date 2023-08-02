from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings

from comments.models import CommentModel
from users.models import UserModel


class BookModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    author = models.ManyToManyField('AuthorModel')
    category = models.ManyToManyField('CategoryModel')
    publishing = models.ManyToManyField('PublishingModel')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    language = models.CharField(verbose_name='Язык', max_length=50, choices=settings.LANGUAGE)
    binding = models.CharField(max_length=50, choices=settings.TYPE_OF_BIND, verbose_name='Тип обложки')
    pages = models.PositiveIntegerField(verbose_name='Количество страниц')
    year = models.PositiveIntegerField(verbose_name='Год издания')
    image = models.ImageField(verbose_name='Изображение', upload_to='books/%Y/%m/%d/',
                              blank=True,
                              default='book-default.png'
                              )
    date_created = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class CategoryModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class AuthorModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']


class PublishingModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'


class ReviewModel(models.Model):
    book = models.ForeignKey(to=BookModel, on_delete=models.CASCADE, verbose_name='Книга')
    user = models.ForeignKey(to=UserModel, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    review = models.TextField(verbose_name='Отзыв')
    comments = GenericRelation(CommentModel, verbose_name='Комментарии')
    create_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'