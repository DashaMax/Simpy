from django.contrib import admin

from blogs.models import BlogModel


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'create_date',
    )


admin.site.register(BlogModel, BlogAdmin)
