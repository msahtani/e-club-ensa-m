from ctypes.wintypes import POINT
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from numpy import put
from responses import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime as dt
from django.http import QueryDict

from .models import *
from .serialisers import *


def fields(T: models.Model):
    return [field.name for field in T._meta.get_fields()]

def postApi(request: HttpRequest, post_id: int):

    if not request.user.is_authenticated:
        return HttpResponseNotFound()

    if request.method == 'GET':
        post_fields = fields(Post)
        
        if post_id != 0:
            try:
                post_ = Post.objects.filter(pk=post_id).values_list(*post_fields)[0]
            except:
                return HttpResponseNotFound()
            post_json ={ 
                key: value
                for key, value in zip(post_fields, post_)
            }
            if post_json["category"] ==  Post.Categories.TRN:
                trs_fields = fields(TrainingSession)
                trs_data = TrainingSession.objects.filter(post=post_).values_list(*trs_fields)[0]
                post_json.update({
                    key: value
                    for key, value in zip(trs_fields, trs_data)
                })
                
            elif ["category"] == Post.Categories.JNS:
                jns_fields = fields(JoiningSession)
                jns_data = JoiningSession.objects.filter(post=post_).values_list(*jns_fields)[0]
                post_json.update({
                    key: value
                    for key, value in zip(jns_fields, jns_data)
                })
            

            return JsonResponse(post_json)
        else:
            posts : Post = Post.objects.filter(approved=True).values_list(*post_fields)
            posts_list = [
                {
                    key: value
                    for key, value in zip(post_fields, post)
                }
                for post in posts
            ]

            for i in range(len(posts)):

                if posts_list[i]["category"] ==  Post.Categories.TRN:
                    trs_fields = fields(TrainingSession)
                    trs_data = TrainingSession.objects.filter(post=posts[i]).values_list(*trs_fields)[0]
                    posts_list[i].update({
                        key: value
                        for key, value in zip(trs_fields, trs_data)
                    })
                
                elif posts_list[i]["category"] == Post.Categories.JNS:
                    jns_fields = fields(JoiningSession)
                    jns_data = JoiningSession.objects.filter(post=posts[i]).values_list(*jns_fields)[0]
                    posts_list[i].update({
                        key: value
                        for key, value in zip(jns_fields, jns_data)
                    })

            return JsonResponse({
                "posts": posts_list
            })
            

    elif request.method == 'POST':

        club_ = get_object_or_404(Club, name=request.POST['club'])

        if not(
            request.POST['title'] 
            and request.POST['content'] 
            and request.POST['club']
        ): return JsonResponse({"message": "title, content and club name are required ... "})

        if not MemberShip.objects.get(
            user=request.user,
            club=club_,
            state=MemberShip.State.ACTIVE
        ): return JsonResponse({"message": "denied ...."})

        post = Post(
            club = club_,
            author = request.user,
            title = request.POST['title'],
            content = request.POST['content']
        )
        post.save()
        return JsonResponse({"message": "created successfully"})
        
    
    elif request.method == 'PUT':


        if not(
            request.POST['title'] 
            and request.POST['content']
        ): return JsonResponse({"message": "title and content are required ... "})

        PUT = QueryDict(request.body)
        data = {
            item: value
            for item, value in PUT.items()
        }
        post = Post.objects.filter(pk=post_id).update(**data)
        
        return JsonResponse({"message": "success!!!"})
        
    elif request.method == r"DELETE":
        post: Post = Post.objects.get(pk=post_id)
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