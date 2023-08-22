from django.contrib import admin

from bot.models import BotChatModel
from utils.admin import MyAdmin


class BotAdmin(MyAdmin):
    list_display = (
        'user',
        'chat_id',
        'create_date',
    )
    fields = (
        'user',
        'chat_id',
        'create_date',
    )
    readonly_fields = (
        'create_date',
    )


admin.site.register(BotChatModel, BotAdmin)
