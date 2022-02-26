from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user, authenticate as auth, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

# Create your views here.


def login_view(request: HttpRequest):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect(next if next else '/')
    elif form.is_bound and not(form.is_valid()):
        return HttpResponse(
            form.errors.as_text(), status=404
        )
    elif form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth(request, username=username, password=password)
        login(request, user)
    
        return redirect(next if next else "/")
    
    context= { 'form': form }
    return render(request, 'login.htm', context)

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')