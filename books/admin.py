from django.contrib import admin

from books.models import (AuthorModel, BookModel, CategoryModel,
                          PublishingModel, ReviewModel)
from utils.admin import MyAdmin


class BookAdmin(MyAdmin):
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }
    list_display = (
        'title',
        'get_html_image',
        'date_created',
    )
    list_display_links = (
        'title',
        'get_html_image'
    )
    fields = (
        'title',
        'slug',
        'image',
        'get_html_image',
        'author',
        'category',
        'publishing',
        'language',
        'binding',
        'pages',
        'year',
        'description',
        'date_created',
    )
    list_filter = (
        'author',
        'category',
        'publishing',
        'language',
        'date_created',
    )
    readonly_fields = (
        'get_html_image',
        'date_created',
    )


class CategoryAdmin(MyAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


class ReviewAdmin(MyAdmin):
    list_display = (
        'book',
        'user',
        'create_date'
    )
    readonly_fields = (
        'create_date',
    )


admin.site.register(BookModel, BookAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(AuthorModel, MyAdmin)
admin.site.register(PublishingModel, MyAdmin)
admin.site.register(ReviewModel, ReviewAdmin)
