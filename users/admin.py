from django.contrib import admin

from users.models import UserModel, CityModel


class UserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'slug',
        'first_name',
        'last_name',
        'email',
        'sex',
        'city',
        'image',
        'date_of_birth',
        'about',
        'book',
        'is_staff'
    )
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'sex',
        'is_staff'
    )


admin.site.register(UserModel, UserAdmin)
admin.site.register(CityModel)
