from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, EmployerProfile, UniversityStaffProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'


class EmployerProfileInline(admin.StackedInline):
    model = EmployerProfile
    can_delete = False
    verbose_name_plural = 'Employer Profile'


class StaffProfileInline(admin.StackedInline):
    model = UniversityStaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if obj.role == 'student':
            return [StudentProfileInline(self.model, self.admin_site)]
        elif obj.role == 'employer':
            return [EmployerProfileInline(self.model, self.admin_site)]
        elif obj.role == 'university_staff':
            return [StaffProfileInline(self.model, self.admin_site)]
        return []


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'department', 'graduation_year']
    list_filter = ['university', 'department']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'contact_phone', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['company_name', 'user__email']


@admin.register(UniversityStaffProfile)
class UniversityStaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'employee_id', 'position']
    list_filter = ['university']
    search_fields = ['user__email', 'employee_id']
