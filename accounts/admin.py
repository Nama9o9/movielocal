from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_pic')}),
    )

admin.site.register(MyUser, MyUserAdmin)