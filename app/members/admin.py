from django.contrib import admin

from .models import User, Mobile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile')
    list_display_links = ('name', 'email', 'mobile')


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    pass
