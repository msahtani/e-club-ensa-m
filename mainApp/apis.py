from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from responses import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime as dt

from .models import *
from .serialisers import *

def postApi(request, post_id: int):

    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == 'GET':
        if post_id != 0:
            post: Post = Post.objects.get(pk=post_id)
            post_json ={ 
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "category" : post.category
            }
            return JsonResponse(post_json)
        else:
            posts : Post = Post.objects.filter(approved=True)
            posts_list = [
                {
                    "club": post.club.name,
                    "title": post.title,
                    "content": post.content,
                    "created_at": post.created_at,
                    "category" : post.category
                }
                for post in posts
            ]

            
            
            return JsonResponse({
                "posts": posts_list
            })
            

    elif request.method == 'POST':
        print(request.POST)
        post = Post(
            club = get_object_or_404(Club, name="club informatique"), # TODO .....

            author = request.user,
            title = request.POST['title'],
            content = request.POST['content']
        )
        post.save()
        return JsonResponse({"message": "Done"})
        
    elif request.method == 'PUT':
        post = Post.objects.get(pk=post_id)
        print(request.headers)
        post.title = request.headers.get("title")
        post.content = request.headers.get("content")
        post.approved = False
        post.save()
        
        return JsonResponse({"message": "success!!!"})
    elif request.method == r"DELETE":
        post = Post.objects.get(pk=post_id)
        post.delete()


def trainingSessionApi(request: HttpRequest, trs_id: int):

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        # create post object
        post_ = Post(
            club = get_object_or_404(Club, name="club informatique"), # TODO .....
            author = request.user,
            title = request.POST['title'],
            content = request.POST['content'],
            category = Post.Categories.TRN
        )
        post_.save()
        
        TrainingSession(
            post = post_,
            limited_places = int(request.POST['limited_places']),
            presented_by = User.objects.get(username= request.POST['presented_by']),
            started_at = make_aware(
                dt.strftime(request.POST['started_at'], '%y-%m-%dT%H:%M')
            )
        ).save()
    
    elif request.method == 'PUT':
        pass


def trainingRegistrationApi(request: HttpRequest, trs_id):
    trs = TrainingSession.objects.get(pk=trs_id)
    if request.method == 'GET':
        records = TrainingRegistration.objects.all()
        data = [
            {
                "user": record.user.username,
                "date_of_reg": record.registered_at
            }
            for record in records
        ]
        return JsonResponse({
            "data": data
        })
    elif request.method == 'POST':

        if trs.limited_places != 0:
            trg_records = TrainingRegistration.objects.filter(session=trs)
            if len(trg_records) == trs.limited_places:
                return JsonResponse({
                    "message": "the limited place was exeeced !!"
                })
        TrainingRegistration(
            session = trs,
            user    = request.user
        ).save()