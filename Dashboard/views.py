from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'welcome.html')


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    return render(request, 'dashboard.html')