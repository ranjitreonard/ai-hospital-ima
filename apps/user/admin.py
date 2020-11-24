from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (_('Login'), {'fields': ('staff_id', 'username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'user_type', 'role', 'status')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staff_id', 'password1', 'password2')
        }),
    )

    list_display = ('staff_id', 'first_name', 'last_name', 'user_type', 'role')

    search_fields = ('staff_id', 'first_name', 'last_name')
    ordering = ('staff_id',)
