from django.http import HttpResponseForbidden
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
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


@login_required
def add_post(request: HttpRequest, club_name: str):
    club = get_object_or_404(Club, name=club_name)
    try:
        member = MemberShip.objects.get(user = request.user, club=club)
    except Exception:
        return HttpResponseForbidden()

    form = PostForm(request.POST or None)
    
    if form.is_valid():
        post = Post()
        post.club = club
        post.author = request.user
        post.title = form.cleaned_data.get('title')
        post.content = form.cleaned_data.get('content')
        post.save()

    context = {
        'form': form,
    }
    
    return render(request, 'add_post.htm', context)


def update_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None)

    if form.is_valid():
        post.author = request.user
        post.title = form.cleaned_data.get('title')
        post.content = form.cleaned_data.get('content')
        post.save()

    context = {
        'form': PostForm({
            'title': post.title,
            'content': post.content
        })
    }

    return render(request, 'add_post.htm', context)