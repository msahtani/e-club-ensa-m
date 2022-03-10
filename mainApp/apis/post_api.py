
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.http import QueryDict
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

from ..models import *


def fields(T: models.Model):
    return [field.name for field in T._meta.get_fields()]



def handle_file_upload(file: InMemoryUploadedFile):
    f = open("helloworld.png", "ab")
    print(f)
    for chunk in file.chunks():
        f.write(chunk)

    f.close()


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
            content = request.POST['content'],
        )

       
        post.main_pic = request.FILES['pic']
        handle_file_upload(request.FILES['pic'])
        

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