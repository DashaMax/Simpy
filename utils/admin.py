from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.safestring import mark_safe


class MyAdmin(admin.ModelAdmin):
    list_per_page = 10
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={
            'rows': 30,
            'cols': 100,
        })},
    }

    def get_html_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='70'>")

    get_html_image.short_description = 'Фото'
