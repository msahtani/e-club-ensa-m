from django.http import JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user, authenticate as auth, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import LoginForm

# Create your views here.


def login_view(request: HttpRequest):
    next = request.GET.get('next')

    if request.user.is_authenticated:
        return redirect(next if next else '/')

    if request.method == "GET":
        return render(request, 'login.htm')
    
    username_ = request.POST['username']
    password_ = request.POST['password']

    if not (username_ and password_):
        JsonResponse({"message": "username and password are required to login "})

    try:
        User.objects.get(username = username_)
    except:
        return JsonResponse({"message": "This user does not exists"})
        

    user = auth(username= username_, password = password_)
    if not user:
        return JsonResponse({"message": "Incorrect password"})
    if not user.is_active:
        return JsonResponse({"message": "This user id not active"})

    login(request, user)
    return redirect(next if next else "/")
    
def signup_view(request: HttpRequest):
    return render(request, 'signup.html')

def forgot_password_view(request:  HttpRequest):
    email = request.GET['email']
    """
    <form method="POST">
        <input type="email" name="email" />
    </form>
    
    """
    user = User.objects.filter()
    
def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')