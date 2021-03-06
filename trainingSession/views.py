from django.shortcuts import render

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from datetime import datetime as dt
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
import uuid

from .models import *
from club.models import Club
from membership.models import MemberShip

from . import ajax

import qrcode
from hashlib import sha256
from uuid import uuid4


class TrainingSessionApi(View):
    
    @method_decorator(login_required)
    def __init__(self, request: HttpRequest = None):
        pass
        # TODO: checking the user permissions .... 
    
    def get(self, request: HttpRequest, club_name):
        if not ajax(request):
            return render(request, "add_training_session.html")

    def post(self, request: HttpRequest, club_name):
        
        club_ = get_object_or_404(Club, name=club_name)
        
        TrainingSession.objects.create(
            club = club_,
            author = request.user,
            title = request.POST['title'],
            content = request.POST['content'],
            category = Post.Categories.TRN,
            main_pic = request.FILES.get('pic'),
            limited_places = int(request.POST['limited_places']),
            presented_by = User.objects.get(username= request.POST['presented_by']),
            started_at = make_aware(
                dt.strptime(request.POST['started_at'], '%Y-%m-%dT%H:%M')
            ),
            approved = True
        )

        return JsonResponse({"message": "success !!! "})
    
    def put(self, request: HttpRequest, trs_id: int):

        PUT = QueryDict(request.body)
        TrainingSession.objects  \
            .filter(pk=trs_id) \
            .update(
                title = PUT['titile'],
                content = PUT['content'],
                limited_places = int(PUT['limited_places']),
                presented_by = User.objects.get(username= PUT['presented_by']),
                started_at = make_aware(
                    dt.strptime(PUT['started_at'], '%Y-%m-%dT%H:%M')
                )
            )

        return JsonResponse({
            'message': 'updated successfully !!'
        })


class TrainingRegistrationApi(View):

    
    def session(self, trs_id):
        return TrainingSession.objects.get(pk=trs_id)


    def get(self, request: HttpRequest, trs_id: int):
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, "register_trs.html")

        records = TrainingRegistration.objects.filter(session = self.session(trs_id))
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


    def post(self, request: HttpRequest, trs_id: int):

        trs: TrainingSession = self.session(trs_id)
        
        if TrainingRegistration.objects.filter(
            user = request.user,
            session = trs
        ).count() == 1: return JsonResponse({
            "message": "you're already regsitered ..... "
        })

        trg_count = TrainingRegistration.objects.filter(session=trs).count()

        if trs.limited_places != 0 and trg_count == trs.limited_places:
            return JsonResponse({
                "message": "the limited places was exeeced !!"
            })
        
        trg: TrainingRegistration = TrainingRegistration.objects.create(
            session = trs,
            user = request.user
        )
        token = uuid.uuid5(uuid.NAMESPACE_URL, trs.created_at)

        trg.token = token
        trg.save()

        URL = request.get_host() + '/trg/confirm?token='+token
        image = qrcode.make(URL)
        image.save(settings.MEDIA_ROOT  + '/images/qrcodes/%s.png' % token)

        return JsonResponse({
            "message": "success !!"
        })
        

def confirm(request: HttpRequest):
    # verfication
    trg = get_object_or_404(
        TrainingRegistration,
        token = request.GET['token']
    )

    if MemberShip.objects.filter(
        user = request.user,
        club = trg.session.club,
    ).filter(
        Q(grade = MemberShip.Grades.PRS) | Q(grade = MemberShip.Grades.VPR)
    ).count == 0: return HttpRequest("permission denied ...")

    if trg.confirmed:
        return HttpResponse("already confirmed ... ")

    trg.confirmed = True
    trg.save()

    return HttpResponse("<h1> confirmed successfully </h1>")