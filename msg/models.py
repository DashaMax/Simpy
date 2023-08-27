from django.db import models


class ChatModel(models.Model):
    members = models.ManyToManyField('users.UserModel', verbose_name='Участники')
    last_message = models.ForeignKey(to='msg.MsgModel', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class MsgModel(models.Model):
    chat = models.ForeignKey(to='msg.ChatModel', on_delete=models.CASCADE, verbose_name='Чат')
    message = models.TextField(verbose_name='Сообщение')
    sender = models.ForeignKey(
        to='users.UserModel',
        on_delete=models.CASCADE,
        verbose_name='Отправитель',
        related_name='Отправитель'
    )
    recipient = models.ForeignKey(
        to='users.UserModel',
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        related_name='Получатель',
    )
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки сообщения')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = (
            'date_time',
        )