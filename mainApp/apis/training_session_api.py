from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.http import QueryDict
from datetime import datetime as dt
import os

from ..models import *
from .post_api import postApi


def trainingSessionApi(request: HttpRequest, trs_id: int):
    
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        # create post object
        postApi(request, 0)
        post_: Post = Post.objects.order_by('created_at')[-1]
        post_.category = Post.Categories.TRN
        post_.save()
        TrainingSession.objects.create(
             post = post_,
            limited_places = int(request.POST['limited_places']),
            presented_by = User.objects.get(username= request.POST['presented_by']),
            started_at = make_aware(
                dt.strftime(request.POST['started_at'], '%y-%m-%dT%H:%M')
            )
        )
        TrainingSession(
           
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