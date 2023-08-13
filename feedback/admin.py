from django.contrib import admin

from feedback.models import FeedbackModel
from utils.admin import MyAdmin


class FeedbackAdmin(MyAdmin):
    list_display = (
        'title',
        'email',
        'is_send',
        'create_date',
    )
    fields = (
        'title',
        'email',
        'feedback',
        'is_send',
        'comments',
        'create_date'
    )
    list_filter = (
        'is_send',
        'create_date',
    )
    readonly_fields = (
        'title',
        'email',
        'feedback',
        'create_date',
    )


admin.site.register(FeedbackModel, FeedbackAdmin)
