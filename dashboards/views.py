from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from accounts.forms import StudentProfileForm, EmployerProfileForm, UserUpdateForm
from jobs.models import Job, Application
from universities.models import University


@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'employer':
        return redirect('employer_dashboard')
    elif role == 'university_staff':
        return redirect('staff_dashboard')
    return redirect('job_list')


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard_redirect')

    try:
        profile = request.user.student_profile
    except Exception:
        profile = None

    applications = Application.objects.filter(student=request.user).select_related('job', 'job__university').order_by('-applied_at')
    stats = {
        'total_applications': applications.count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'hired': applications.filter(status='hired').count(),
        'rejected': applications.filter(status='rejected').count(),
    }

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = StudentProfileForm(instance=profile)

    return render(request, 'dashboards/student_dashboard.html', {
        'profile': profile,
        'applications': applications[:5],
        'stats': stats,
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Student Dashboard',
    })


@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        return redirect('dashboard_redirect')

    try:
        profile = request.user.employer_profile
    except Exception:
        profile = None

    jobs = Job.objects.filter(employer=request.user).annotate(app_count=Count('applications'))
    stats = {
        'total_jobs': jobs.count(),
        'approved_jobs': jobs.filter(approval_status='approved').count(),
        'pending_jobs': jobs.filter(approval_status='pending').count(),
        'total_applications': Application.objects.filter(job__employer=request.user).count(),
    }

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('employer_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = EmployerProfileForm(instance=profile)

    return render(request, 'dashboards/employer_dashboard.html', {
        'profile': profile,
        'jobs': jobs,
        'stats': stats,
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Employer Dashboard',
    })


@login_required
def staff_dashboard(request):
    if request.user.role != 'university_staff':
        return redirect('dashboard_redirect')

    try:
        profile = request.user.staff_profile
        university = profile.university
    except Exception:
        messages.error(request, 'No university profile found.')
        return redirect('job_list')

    pending_jobs = Job.objects.filter(university=university, approval_status='pending')
    all_jobs = Job.objects.filter(university=university).annotate(app_count=Count('applications'))
    applications = Application.objects.filter(job__university=university).select_related('student', 'job')
    stats = {
        'total_jobs': all_jobs.count(),
        'pending_jobs': pending_jobs.count(),
        'approved_jobs': all_jobs.filter(approval_status='approved').count(),
        'total_applications': applications.count(),
    }

    return render(request, 'dashboards/staff_dashboard.html', {
        'profile': profile,
        'university': university,
        'pending_jobs': pending_jobs,
        'all_jobs': all_jobs,
        'applications': applications[:10],
        'stats': stats,
        'title': 'University Staff Dashboard',
    })


@login_required
def approve_job(request, pk):
    if request.user.role != 'university_staff':
        return redirect('dashboard_redirect')
    job = get_object_or_404(Job, pk=pk, university=request.user.staff_profile.university)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            job.approval_status = 'approved'
            job.is_approved = True
            job.approved_by = request.user
            messages.success(request, f'Job "{job.title}" approved.')
        elif action == 'reject':
            job.approval_status = 'rejected'
            job.is_approved = False
            messages.warning(request, f'Job "{job.title}" rejected.')
        job.save()
    return redirect('staff_dashboard')
