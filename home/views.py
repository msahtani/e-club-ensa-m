from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from post.models import Article
from trainingSession.models import TrainingSession
from membership.models import JoiningSession
from club.models import Club

from utils import fields

def get_feeds():
    
    pass



def home_view(request: HttpRequest):
    return render(request, 'home.html')

@login_required
def club_profile(request: HttpRequest, club_name: str):
    get_object_or_404(Club, name=club_name)
    
    return render(request, 'club_profile.htm')

def update_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Article, pk=post_id)

    if post.author != request.user:
        return HttpResponse(code=403)

    return render(request, 'update_post.htm')

def get_articles():
    fld = fields(Article, exclude=['approved'])
    record = Article.objects.filter(
        approved = True
    ).values_list(*fld)

    json_data = {
        key: value
        for key, value in zip(fld, record)
    }