from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models.users import User
from .models.verification_code import VerificationCode

class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'user',
        'email_verification_code',
        'phone_verification_code',
        'email_verified',
        'phone_verified',
        'created_at',
        'is_active'
    )
    search_fields = (
        'code',
        'email_verification_code',
        'phone_verification_code'
    )
    ordering = ('-created_at',)
    
    def code(self, obj):
        # Return one of the verification codes as the display value for 'code'
        return obj.email_verification_code or obj.phone_verification_code

    def is_active(self, obj):
        # Consider the verification code active if at least one code is not expired.
        email_active = True if not obj.email_verification_code_expiry else (timezone.now() <= obj.email_verification_code_expiry)
        phone_active = True if not obj.phone_verification_code_expiry else (timezone.now() <= obj.phone_verification_code_expiry)
        return email_active or phone_active

admin.site.register(VerificationCode, VerificationCodeAdmin)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'firstName', 'lastName', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('firstName', 'lastName', 'phoneNumber', 'gender', 'userRole')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Banning', {'fields': ('isBanned', 'banReason', 'limitedBan', 'limitedBanTime')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2'),
        }),
    )
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
