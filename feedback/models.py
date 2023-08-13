from django.db import models


class FeedbackModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема обращения')
    email = models.EmailField(max_length=150, verbose_name='E-mail для связи')
    feedback = models.TextField(verbose_name='Сообщение')
    is_send = models.BooleanField(verbose_name='Отправил ответное письмо', default=False)
    comments = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания обращения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = (
            '-create_date',
        )