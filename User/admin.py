from django.contrib import admin
from .models import User
from import_export.admin import ImportExportModelAdmin

class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'matric_number', 'staff_id', 
        'user_type', 'verified_staff', 'date_joined' 
    ]

    list_filter = [
        'user_type', 'is_active', 'is_staff', 'date_joined', 
        'verified_staff',
    ]

    search_fields = [
        'matric_number', 'first_name', 'middle_name', 'last_name',
        'serial_number'
    ]

admin.site.register(User, UserAdmin)