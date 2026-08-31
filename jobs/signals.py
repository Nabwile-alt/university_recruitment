from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, Application
from notifications.utils import send_notification_email


@receiver(post_save, sender=Job)
def notify_staff_on_job_post(sender, instance, created, **kwargs):
    if created:
        from accounts.models import UniversityStaffProfile
        staff_profiles = UniversityStaffProfile.objects.filter(university=instance.university)
        for profile in staff_profiles:
            send_notification_email(
                to_email=profile.user.email,
                subject=f'New Job Posting Requires Approval: {instance.title}',
                template='notifications/email/job_posted.txt',
                context={
                    'staff_name': profile.user.get_full_name(),
                    'job_title': instance.title,
                    'employer': instance.employer.get_full_name(),
                    'university': instance.university.name,
                }
            )


@receiver(post_save, sender=Job)
def notify_employer_on_approval(sender, instance, created, **kwargs):
    if not created and instance.approval_status == 'approved':
        send_notification_email(
            to_email=instance.employer.email,
            subject=f'Your Job Posting "{instance.title}" Has Been Approved',
            template='notifications/email/job_approved.txt',
            context={
                'employer_name': instance.employer.get_full_name(),
                'job_title': instance.title,
                'university': instance.university.name,
            }
        )


@receiver(post_save, sender=Application)
def notify_employer_on_application(sender, instance, created, **kwargs):
    if created:
        send_notification_email(
            to_email=instance.job.employer.email,
            subject=f'New Application for "{instance.job.title}"',
            template='notifications/email/application_received.txt',
            context={
                'employer_name': instance.job.employer.get_full_name(),
                'job_title': instance.job.title,
                'applicant_name': instance.student.get_full_name(),
                'applicant_email': instance.student.email,
            }
        )


@receiver(post_save, sender=Application)
def notify_student_on_status_change(sender, instance, created, **kwargs):
    if not created:
        send_notification_email(
            to_email=instance.student.email,
            subject=f'Application Status Update: {instance.job.title}',
            template='notifications/email/status_changed.txt',
            context={
                'student_name': instance.student.get_full_name(),
                'job_title': instance.job.title,
                'status': instance.get_status_display(),
                'employer': instance.job.employer.employer_profile.company_name,
            }
        )
