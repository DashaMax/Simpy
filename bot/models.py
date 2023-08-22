from django.db import models


class BotChatModel(models.Model):
    user = models.OneToOneField(
        to='users.UserModel',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    chat_id = models.PositiveIntegerField(unique=True, verbose_name='ID чата в телеграме', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    def __str__(self):
        return str(self.chat_id)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = (
            '-create_date',
        )