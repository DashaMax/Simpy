from django.contrib import admin

from blogs.models import BlogModel


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'create_date',
    )


admin.site.register(BlogModel, BlogAdmin)
