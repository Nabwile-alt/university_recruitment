from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'university', 'department', 'job_type', 'approval_status', 'is_active', 'created_at']
    list_filter = ['job_type', 'approval_status', 'is_active', 'university', 'department']
    search_fields = ['title', 'employer__email', 'university__name', 'department__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['approval_status', 'is_active']
    date_hierarchy = 'created_at'
    actions = ['approve_jobs', 'reject_jobs']

    def approve_jobs(self, request, queryset):
        queryset.update(approval_status='approved', is_approved=True)
        self.message_user(request, 'Selected jobs approved.')
    approve_jobs.short_description = 'Approve selected jobs'

    def reject_jobs(self, request, queryset):
        queryset.update(approval_status='rejected', is_approved=False)
        self.message_user(request, 'Selected jobs rejected.')
    reject_jobs.short_description = 'Reject selected jobs'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'applied_at']
    list_filter = ['status', 'job__university', 'job__department']
    search_fields = ['student__email', 'job__title']
    readonly_fields = ['applied_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'applied_at'
