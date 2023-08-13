from django.contrib import admin

from comments.models import CommentModel
from utils.admin import MyAdmin


class CommentAdmin(MyAdmin):
    list_display = (
        'user',
        'content_type',
        'comment',
        'create_date',
    )
    list_display_links = (
        'user',
        'comment'
    )
    fields = (
        'user',
        'content_type',
        'object_id',
        'comment',
        'create_date',
    )
    list_filter = (
        'user',
        'content_type',
        'create_date',
    )
    readonly_fields = (
        'create_date',
    )


admin.site.register(CommentModel, CommentAdmin)