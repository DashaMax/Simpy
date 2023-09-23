from django.contrib import admin

from msg.models import ChatModel, MsgModel
from utils.admin import MyAdmin


class ChatAdmin(MyAdmin):
    list_display = (
        'pk',
        'last_message',
    )
    fields = (
        'pk',
        'members',
        'last_message',
    )
    list_filter = (
        'members',
        'last_message',
    )
    readonly_fields = (
        'pk',
    )


class MsgAdmin(MyAdmin):
    list_display = (
        'sender',
        'recipient',
        'is_read',
        'date_time',
    )
    fields = (
        'chat',
        'sender',
        'recipient',
        'message',
        'is_read',
        'date_time',
    )
    list_filter = (
        'is_read',
        'date_time',
    )
    readonly_fields = (
        'date_time',
    )


admin.site.register(MsgModel, MsgAdmin)
admin.site.register(ChatModel, ChatAdmin)
