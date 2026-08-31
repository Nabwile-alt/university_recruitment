from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, EmployerRegistrationForm, StaffRegistrationForm


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Student account created successfully!')
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form, 'title': 'Student Registration'})


def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Employer account created successfully!')
            return redirect('employer_dashboard')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'accounts/register_employer.html', {'form': form, 'title': 'Employer Registration'})


def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'University Staff account created successfully!')
            return redirect('staff_dashboard')
    else:
        form = StaffRegistrationForm()
    return render(request, 'accounts/register_staff.html', {'form': form, 'title': 'Staff Registration'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html', {'title': 'Login'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
