from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Mobile

admin.site.register(User, UserAdmin)


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    pass
