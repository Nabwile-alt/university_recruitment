from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notifications_home(request):
    return render(request, 'notifications/home.html', {'title': 'Notifications'})
