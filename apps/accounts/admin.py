from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.users import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'firstName', 'lastName', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('firstName', 'lastName', 'phoneNumber', 'gender', 'userRole')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'createdAt', 'updatedAt')}),
        ('Banning', {'fields': ('isBanned', 'banReason', 'limitedBan', 'limitedBanTime')}),
    )
    readonly_fields = ('createdAt', 'updatedAt', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2'),
        }),
    )
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
