from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.http import QueryDict
from datetime import datetime as dt
from django.views import View

from ..models import *
from .post_api import PostApi


class ClubApi(View):

    def __init__(self):
        pass

    def get(self, request: HttpRequest, club_name):
        
        club_: Club = Club.objects.get(name=club_name)
        memebers = MemberShip.objects.filter(
            club=club_, cell=None
        )

        json_data = {
            "name": club_.name,
            "desc": club_.description,
            "logo": "/media/" + str(club_.logo),
            "board_members": {
                key: str(User.objects.get(pk=value))
                for key, value
                in memebers.values_list('grade', 'user')
            }, "cells": {
                str(cell_): str(MemberShip.objects.get(grade = MemberShip.Grades.CLM, cell=cell_)).split(' --')[0]
                for cell_ in Cell.objects.filter(club=club_)
            }, "posts": {
                
            }
        
        }


        return JsonResponse(json_data)

    def post(self, request: HttpRequest):
        pass

    def put(self, request: HttpRequest, club_name):
        PUT = QueryDict(request.body)
        Club.objects.filter(name=club_name).update(
            **PUT, logo = request.FILES.get('logo')
        )
       
        return JsonResponse({
            'message': 'updated successfully'
        })
        
    def delete(self, request):
        pass


class CellApi(View):

    def __init__(self, request, club_name):
        self.club = Club.objects.get(name=club_name)

    def get(self, request: HttpRequest, club_name):
        cells = Cell.objects.filter(
            club = self.club
        )

        json_data = {
            "cells": {
                str(cell_): str(MemberShip.objects.get(grade = MemberShip.Grades.CLM, cell=cell_)).split(' --')[0]
                for cell_ in cells
            }
        }
        return JsonResponse(json_data)

    def post(self, request: HttpRequest, club_name):

        if Cell.objects.filter(club = self.club, name=request.POST['name']).count != 0:
            return JsonResponse({
                'message':  'this name is already exists ...'
            })

        cell = Cell(
            **request.POST,
            club= self.club
        ).save()

        # TODO : assign a cell manager
        
        return JsonResponse({
            "message": '"{}"' % cell.name + "is created successfully"
        })

    def put(self, request: HttpRequest, club_name, cell_name):
        
        PUT = QueryDict(request.body)

        cell = Cell.objects.filter(
            club = Club.objects.get(name=club_name),
            name = cell_name
        ).update(**PUT)

        # TODO : change the cell manager
        return JsonResponse({
            "message": "updated successfully"
        })
    def delete(self, request: HttpRequest):
        pass