from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views import View

class UserApi(View):

    def get(self, request: HttpRequest):
        if request.GET['username'] == '':
            return JsonResponse({"users": []})
            
        users_record = User.objects.filter(username__startswith = request.GET['username'])
       
        return JsonResponse({"users": [
            user.username for user in users_record
        ]})