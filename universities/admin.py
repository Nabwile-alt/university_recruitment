from django.contrib import admin
from .models import University, Department


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'founded_year', 'created_at']
    search_fields = ['name', 'address']
    inlines = [DepartmentInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'head']
    list_filter = ['university']
    search_fields = ['name', 'university__name']
