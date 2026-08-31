from django.urls import path
from . import views

urlpatterns = [
    path('redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/jobs/<int:pk>/approve/', views.approve_job, name='approve_job'),
]
