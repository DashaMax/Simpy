from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentModel(models.Model):
    user = models.ForeignKey(to='users.UserModel', on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    comment = models.CharField(max_length=150, verbose_name='Комментарий')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип контента')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'