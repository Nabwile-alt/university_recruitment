from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('employer/jobs/', views.employer_jobs, name='employer_jobs'),
    path('employer/jobs/create/', views.create_job, name='create_job'),
    path('employer/jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('employer/jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('employer/jobs/<int:pk>/applicants/', views.job_applicants, name='job_applicants'),
    path('employer/applications/<int:pk>/status/', views.update_application_status, name='update_application_status'),
]
