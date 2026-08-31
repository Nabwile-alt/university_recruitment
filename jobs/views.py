from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm, JobSearchForm, ApplicationStatusForm


def job_list(request):
    jobs = Job.objects.filter(is_approved=True, is_active=True).select_related('university', 'department', 'employer')
    form = JobSearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        university = form.cleaned_data.get('university')
        department = form.cleaned_data.get('department')
        job_type = form.cleaned_data.get('job_type')
        if keyword:
            jobs = jobs.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        if university:
            jobs = jobs.filter(university=university)
        if department:
            jobs = jobs.filter(department=department)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'form': form, 'title': 'Job Listings'})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_approved=True, is_active=True)
    already_applied = False
    if request.user.is_authenticated and request.user.role == 'student':
        already_applied = Application.objects.filter(job=job, student=request.user).exists()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'title': job.title,
    })


@login_required
def apply_job(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can apply to jobs.')
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk, is_approved=True, is_active=True)

    if Application.objects.filter(job=job, student=request.user).exists():
        messages.warning(request, 'You have already applied to this job.')
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('student_dashboard')
    else:
        # Pre-fill resume if student has one
        try:
            profile = request.user.student_profile
            form = ApplicationForm(initial={'resume': profile.resume})
        except Exception:
            form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job, 'title': 'Apply for Job'})


@login_required
def employer_jobs(request):
    if request.user.role != 'employer':
        return redirect('job_list')
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'jobs/employer_jobs.html', {'jobs': jobs, 'title': 'My Job Postings'})


@login_required
def create_job(request):
    if request.user.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted! Awaiting university staff approval.')
            return redirect('employer_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post a Job'})


@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job', 'job': job})


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
        return redirect('employer_jobs')
    return render(request, 'jobs/confirm_delete.html', {'job': job, 'title': 'Delete Job'})


@login_required
def job_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    applications = job.applications.select_related('student').all()
    return render(request, 'jobs/applicants.html', {'job': job, 'applications': applications, 'title': 'Applicants'})


@login_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated.')
    return redirect('job_applicants', pk=application.job.pk)
