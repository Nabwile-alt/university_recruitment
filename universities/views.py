from django.shortcuts import render, get_object_or_404
from .models import University, Department
from jobs.models import Job


def university_list(request):
    universities = University.objects.all()
    return render(request, 'universities/university_list.html', {'universities': universities})


def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    departments = university.departments.all()
    jobs = Job.objects.filter(university=university, is_approved=True, is_active=True)
    return render(request, 'universities/university_detail.html', {
        'university': university,
        'departments': departments,
        'jobs': jobs,
    })
