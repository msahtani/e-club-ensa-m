from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user, authenticate as auth, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

# Create your views here.

@login_required
def home_view(request: HttpRequest):

    context= {
        'user': get_user(request),
        'is_logged_in': not isinstance(get_user(request), AnonymousUser)
    }
    return render(request, 'home.htm', context)

def login_view(request: HttpRequest):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth(request, username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context= { 'form': form }
    return render(request, 'login.htm', context)

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')