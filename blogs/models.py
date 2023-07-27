from django.db import models
from pytils.translit import slugify


class BlogModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL', blank=True)
    author = models.ForeignKey(to='users.UserModel', on_delete=models.DO_NOTHING, verbose_name='Автор')
    image = models.ImageField(upload_to='blog/%Y/%m/%d/', verbose_name='Фото', default='blog-main.jpg')
    description = models.TextField(verbose_name='Блог')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'