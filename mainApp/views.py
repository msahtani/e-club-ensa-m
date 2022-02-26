from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user, authenticate as auth, login, logout
from django.contrib.auth.decorators import *

from .forms import *
from .models import Post


# Create your views here.

def home_view(request: HttpRequest):
    posts = Post.objects.all()
    context= {
        'user': get_user(request) if request.user.is_authenticated else None,
        'posts': posts
    }
    return render(request, 'home.html', context)



# TODO : ......................
@login_required
def add_post(request: HttpRequest, club: str):
    form = addPostForm(request.POST or None)
    
    if form.is_valid():
        post = Post()
        post.club = Club.objects.get(name=club)
        post.author = request.user
        post.title = form.cleaned_data.get('title')
        post.content = form.cleaned_data.get('content')
        post.save()

    context = {
        'form': form,
        'user': "mohcine"
    }
    
    return render(request, 'add_post.htm', context)