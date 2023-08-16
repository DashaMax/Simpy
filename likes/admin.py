from django.contrib import admin

from likes.models import LikeModel
from utils.admin import MyAdmin


class LikeAdmin(MyAdmin):
    list_display = (
        'user',
        'content_type',
        'is_like',
    )
    list_display_links = (
        'user',
        'is_like'
    )
    fields = (
        'user',
        'content_type',
        'object_id',
        'is_like',
    )
    list_filter = (
        'user',
        'content_type',
        'is_like',
    )


admin.site.register(LikeModel, LikeAdmin)