from django.http import HttpResponseForbidden, JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.contrib.auth.decorators import *
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Club


# Create your views here.

def home_view(request: HttpRequest):
    return render(request, 'home.html')

@login_required
def club_profile(request: HttpRequest, club_name: str):
    get_object_or_404(Club, name=club_name)
     
    return render(request, 'club_profile.htm')



def update_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return HttpResponse(code=403)

    return render(request, 'update_post.htm')