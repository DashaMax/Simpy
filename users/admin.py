from django.contrib import admin

from users.models import CityModel, UserModel
from utils.admin import MyAdmin


class UserAdmin(MyAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'get_html_image',
        'email',
        'sex',
        'is_staff',
    )
    list_display_links = (
        'username',
        'get_html_image'
    )
    fields = (
        'username',
        'slug',
        'first_name',
        'last_name',
        'email',
        'sex',
        'city',
        'image',
        'get_html_image',
        'date_of_birth',
        'about',
        'book',
        'is_send_notifications',
        'is_staff',
        'groups',
    )
    list_filter = (
        'sex',
        'city',
        'is_staff'
    )
    readonly_fields = (
        'slug',
        'get_html_image',
    )


admin.site.register(UserModel, UserAdmin)
admin.site.register(CityModel, MyAdmin)
