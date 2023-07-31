from django.contrib import admin

from quotes.models import QuoteModel


class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'create_date',
    )


admin.site.register(QuoteModel, QuoteAdmin)

