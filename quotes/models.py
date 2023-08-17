from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from comments.models import CommentModel
from likes.models import LikeModel


class QuoteModel(models.Model):
    user = models.ForeignKey(to='users.UserModel', on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    book = models.ForeignKey(to='books.BookModel', on_delete=models.DO_NOTHING, verbose_name='Книга')
    quote = models.TextField(verbose_name='Цитата')
    comments = GenericRelation(CommentModel)
    likes = GenericRelation(LikeModel)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.quote

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        ordering = (
            '-create_date',
        )

    def get_count_likes(self):
        return len(self.likes.filter(is_like=True))