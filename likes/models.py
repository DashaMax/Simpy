from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikeModel(models.Model):
    user = models.ForeignKey(to='users.UserModel', on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    is_like = models.BooleanField(default=False, verbose_name='Поставлен лайк')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип контента')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.is_like)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'