from django.contrib import admin
from .models import (CustomUser, CustomUser, Partner, 
                     StaffUser, PhoneNumber, Profile)
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'is_superuser',
                'is_partner',
                'is_customer',
            ),
        }),
    )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Partner)
admin.site.register(StaffUser)
admin.site.register(Profile)
admin.site.register(PhoneNumber)
