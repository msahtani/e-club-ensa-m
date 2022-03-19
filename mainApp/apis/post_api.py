
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.http import QueryDict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views import View
import os

from ..models import *


def fields(T: models.Model):
    return [field.name for field in T._meta.get_fields()]


class PostApi(View):

    def __init__(self, request: HttpRequest = None, post_id: int = None):
        if not request:
            return

        if request.method == 'GET':
            self.get(request, post_id)
        elif request.method == 'POST':
            self.post(request, post_id)
        elif request.method == 'PUT':
            self.put(request, post_id)
        elif request.method == r'DELETE':
            self.delete(request, post_id)

    def get(self, request: HttpRequest, post_id):
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
            
            
            return JsonResponse(post_json)
            
        else:
            posts : Post = Post.objects.all().values_list(*post_fields)
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
            
    def post(self, request:HttpRequest, club_name):

        club_ = get_object_or_404(Club, name=club_name)

        if not(
            request.POST.get('title') 
            and request.POST.get('content') 
        ): return JsonResponse({"message": "title and content are required ... "})

        if not MemberShip.objects.get(
            user=request.user,
            club=club_,
            state=MemberShip.State.ACTIVE
        ): return JsonResponse({"message": "denied ...."})

        post = Post.objects.create(
            club = club_,
            author = request.user,
            title = request.POST['title'],
            content = request.POST['content'],
            main_pic = request.FILES.get('pic')
        )
        return JsonResponse({
            "message": "created successfully",
            "id": post.id_post
        })
        
    def put(self, request:HttpRequest, post_id):

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
        
    def delete(self, request:HttpRequest, post_id):
        post: Post = Post.objects.get(pk=post_id)
        post.delete()