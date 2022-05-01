from django.http import request, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate as auth, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *


def login_view(request: request.HttpRequest):
    next = request.GET.get('next')

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(next if next else '/')
        return render(request, 'login.htm')
    
    username_ = request.POST.get('username')
    password_ = request.POST.get('password')

    if not (username_ and password_):
        JsonResponse({"message": "username and password are required to login "})

    try:
        Student.objects.get(username = username_)
    except:
        return JsonResponse({"message": "This user does not exists"})
        
    user = auth(username= username_, password = password_)
    if not user:
        return JsonResponse({"message": "Incorrect password"})
    if not user.is_active:
        return JsonResponse({"message": "This user id not active"})

    login(request, user)
    return redirect(next if next else "/")
    
def signup_view(request: request.HttpRequest):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'signup.html')

    user = Student(
        first_name = request.POST['firstname'],
        last_name = request.POST['lastname'],
        email = request.POST['email'],
    )
    user.set_password(request.POST['password'])
    user.save()

    login(request, user)

    return JsonResponse({"message": "created successfully ... "})

@csrf_exempt
def forgot_password_view(request: request.HttpRequest):

    if request.method == 'GET':
        return render(request, 'forgotten_password.html')

    inp = request.POST.get('email_or_usrname')
    user = Student.objects.filter(
        Q(email = inp) | Q(username= inp) 
    )
    if user.count() == 0:
        return JsonResponse({'message': '.....'})
    
    ResetPasswordTokens.objects.create(user = user[0])

    return JsonResponse({'message': '......'})

@csrf_exempt
def reset_password_view(request: request.HttpRequest):
    rptoken: ResetPasswordTokens
    try:
        rptoken = ResetPasswordTokens.objects.filter(
            token = request.GET.get('token')
        )[0]
    except:
        return JsonResponse({'message': "the token doesn't exist"})
    
    if rptoken.expired():
        return JsonResponse({'message': "the token is expired"})

    if request.method == 'GET':
        return render(request, 'reset_password.html')

    std = rptoken.get_user()
    std.set_password(request.POST['password'])
    std.save()
    login(request, std)
    rptoken.delete()
    return JsonResponse({'message': 'reseted successfully'})

def logout_view(request: request.HttpRequest):
    logout(request)
    return redirect('/')
