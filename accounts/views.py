from django.conf import settings
from django.http import request, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate as auth, login, logout
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from .models import *
import uuid

def login_view(request: request.HttpRequest):
    next = request.GET.get('next')

    if request.user.is_authenticated:
        return redirect(next if next else '/')

    if request.method == "GET":
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

    # check if the user is authenticated ... 
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'signup.html')

    fname, lname = request.POST['firstname'], request.POST['lastname']
    username_ = fname.replace(' ', '_') + '_' + lname.replace(' ', '_')
    username_ = username_.lower() # to lowercase 
    password = request.POST['password']
    user = Student(
        first_name = fname,
        last_name = lname,
        username = username_,
        email = request.POST['email']
    )
    user.set_password(password)
    user.save()

    login(request, user)

    return JsonResponse({"message": "created successfully ... "})

@csrf_exempt
def forgot_password_view(request: request.HttpRequest):

    if request.method == 'GET':
        return render(request, 'forgotten_password.html')

    email_ = request.POST.get('email')
    user = Student.objects.filter(email = email_)

    if user.count() == 0:
        return JsonResponse({'message': 'this email is incorrect'})
    
    user: Student = user[0]
    # TODO : sending a email to this user contains a token
    token = uuid.uuid5(uuid.NAMESPACE_URL, user.email).hex
    send_reset_password_token(request.get_host(), token, user.email)
    
    ResetPasswordTokens.objects.create(
        user = user,
        token = token,
    )

    return JsonResponse({'message': 'sent successfully'})

@csrf_exempt
def reset_password_view(request: request.HttpRequest):
    record = ResetPasswordTokens.objects.filter(
        token = request.GET.get('token'))
    
    if record.count() == 0:
        return JsonResponse({'message': "the token doesn't exist"})

    rptoken: ResetPasswordTokens = record[0]

    if rptoken.expired():
        rptoken.delete()
        return JsonResponse({'message': "the token is expired"})

    if request.method == 'GET':
        return render(request, 'reset_password.html')

    password, rpassword = request.POST.get('password'), request.POST.get('rpassword')
    if password != rpassword:
        return JsonResponse({'message': "these passwords doesn't match"})

    std: Student = rptoken.user
    std.set_password(password)
    std.save()
    login(request, std)
    rptoken.delete()
    return JsonResponse({'message': 'reseted successfully'})

def logout_view(request: request.HttpRequest):
    logout(request)
    return redirect('/')

def send_reset_password_token(host, token, to):
    SUBJECT = 'reset password demo'
    LINK = host + f'/reset_password?token={token}'
    BODY = f"to reset your password, click to the link below \n {LINK}"

    send_mail(
        SUBJECT,
        BODY,
        settings.EMAIL_HOST_USER,
        [to]
    )