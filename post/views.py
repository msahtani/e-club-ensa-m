from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from utils import *

from .models import *
from accounts.models import Student
from membership.models import *

import os


@method_decorator(csrf_exempt, name='dispatch')
class ArticleApi(View):


    def get(self, request: HttpRequest, club_name, post_id=0):
        article_fields = fields(Article)
        
        if post_id != 0:
            try:
                post_ = Post.objects.filter(pk=post_id).values_list(*article_fields)[0]
            except:
                return HttpResponseNotFound()
                
            post_json ={ 
                key: value
                for key, value in zip(article_fields, post_)
            }
            
            return JsonResponse(post_json)
            
        else:
            posts : Article = Article.objects.all().values_list(*article_fields)
            posts_list = [
                {
                    key: value
                    for key, value in zip(article_fields, post)
                }
                for post in posts
            ]

    
            return JsonResponse({
                "articles": posts_list
            })
    
    def post(self, request:HttpRequest, club_name):


        club_ = get_object_or_404(Club, name=club_name)

        if not(
            request.POST.get('title') 
            and request.POST.get('content') 
        ): return JsonResponse({"message": "title and content are required ... "})

        # if MemberShip.objects.filter(
        #     user=request.user,
        #     club=club_,
        #     state=MemberShip.State.ACTIVE
        # ).count() == 0: return JsonResponse({"message": "denied ...."})

        article = Article.objects.create(
            club = club_,
            author = Student.objects.get(username='sahcine'),
            title = request.POST['title'],
            content = request.POST['content'],
            main_pic = request.FILES.get('pic')
        )
        return JsonResponse({
            "message": "created successfully",
            "id": article.pk
        })
        
    def put(self, request:HttpRequest, article_id):


        PUT = QueryDict(request.body)
        
        data = {
            item: value
            for item, value in PUT.items()
        }
        post: Article = Article.objects.filter(
            pk=article_id).update(**data)

        if request.FILES.get('pic'):
            post.main_pic = request.FILES.get('pic')
            post.save()

        return JsonResponse({"message": "success!!!"})
        
    def delete(self, request:HttpRequest, post_id):
        post: Post = Post.objects.get(pk=post_id)
        post.delete()

def update_post_view(request: HttpRequest, post_id):

    if Post.objects.filter(
        pk = post_id,
        author = request.user
    ).count() == 0:
        return HttpResponse("<h1> ERROR 403 HTTPS : FORBIDDEN </h1>")


    return render(request, 'update_post.html')