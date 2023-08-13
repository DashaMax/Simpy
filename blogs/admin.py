from django.contrib import admin

from blogs.models import BlogModel
from utils.admin import MyAdmin


class BlogAdmin(MyAdmin):
    list_display = (
        'title',
        'user',
        'get_html_image',
        'create_date',
    )
    list_display_links = (
        'title',
        'get_html_image'
    )
    fields = (
        'title',
        'slug',
        'user',
        'image',
        'get_html_image',
        'blog',
        'create_date'
    )
    list_filter = (
        'user',
        'create_date'
    )
    readonly_fields = (
        'slug',
        'get_html_image',
        'create_date'
    )


admin.site.site_title = 'Simpy - админ-панель'
admin.site.site_header = 'Simpy - админ-панель'
admin.site.register(BlogModel, BlogAdmin)
