from django.contrib import admin

from quotes.models import QuoteModel
from utils.admin import MyAdmin


class QuoteAdmin(MyAdmin):
    list_display = (
        'user',
        'book',
        'create_date',
    )
    list_filter = (
        'user',
        'book',
        'create_date',
    )


admin.site.register(QuoteModel, QuoteAdmin)

