from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role', 'employee_id', 'full_name')}),
    )
    list_display = ['email', 'username', 'role', 'is_staff']

admin.site.register(User, CustomUserAdmin)

