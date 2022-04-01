from django.http import JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user, authenticate as auth, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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

    # check if the user is authenticated ... 
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'signup.html')

    fname, lname = request.POST['firstname'], request.POST['lastname']
    username_ = fname.replace(' ', '_') + '_' + lname.replace(' ', '_')
    username_ = username_.lower() # to lowercase 
    password = request.POST['password']
    user = User(
        first_name = fname,
        last_name = lname,
        username = username_,
        email = request.POST['email']
    )

    user.set_password(password)
    user.save()

    login(request, user)

    return JsonResponse({"message": "created successfully ... "})


    

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