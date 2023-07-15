from django.contrib import admin

from books.models import BookModel, CategoryModel, AuthorModel, PublishingModel


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
    readonly_fields = ('date_created',)
    list_display = (
        'title',
        'date_created'
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(BookModel, BookAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(AuthorModel)
admin.site.register(PublishingModel)
