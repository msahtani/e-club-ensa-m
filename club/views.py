from django.shortcuts import render

from django.http import HttpRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.http import QueryDict
from datetime import datetime as dt
from django.views import View

from utils import ajax

from .models import *
from membership.models import MemberShip


class ClubApi(View):

    def get(self, request: HttpRequest, club_name):

        if not ajax(request):
            return render(request, 'club_profile.htm')
        
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

    def club(club_name):
        return  Club.objects.get(name=club_name)

    def get(self, request: HttpRequest, club_name):
        # get cells of the given club object
        cells = Cell.objects.filter(
            club = self.club(club_name)
        )
        # from ORM to JSON
        json_data = {
            "cells": {
                str(cell_): str(MemberShip.objects.get(grade = MemberShip.Grades.CLM, cell=cell_)).split(' --')[0]
                for cell_ in cells
            }}
        # send the JSON DATA
        return JsonResponse(json_data)

    def post(self, request: HttpRequest, club_name):

        if Cell.objects.filter(club = self.club(club_name), name=request.POST['name']).count != 0:
            return JsonResponse({
                'message':  'this name is already exists ...'
            })

        cell_ = Cell.objects.create(
            **request.POST,
            club= self.club(club_name)
        )

        # TODO : assign a cell manager
        self.assign_cell_manager(cell_, request.POST['username'])
        
        return JsonResponse({
            "message": '"%s"' % cell_.name + "is created successfully"
        })

    def put(self, request: HttpRequest, club_name, cell_name):
        
        PUT = QueryDict(request.body)

        cell_ = Cell.objects.filter(
            club = Club.objects.get(name=club_name),
            name = cell_name
        ).update(**PUT)

        self.assign_cell_manager(cell_, PUT['username'])
        
        return JsonResponse({
            "message": "updated successfully"
        })

    
    def delete(self, request: HttpRequest, club_name, cell_name):
        cell: Cell = Cell.objects.get(
            club = self.club(club_name),
            name = cell_name
        )
        cell.delete()
        

    def assign_cell_manager(self, cell_: Cell, username_):
        user_ = User.objects.get(username = username_)
        cell_members = MemberShip.objects.filter(
            club = self.club,
            cell = cell_
        )

        if cell_members.filter(grade = MemberShip.Grades.CLM).count() == 0:
            if cell_members.filter(user = user_).count() == 0:
                cell_members.create(
                    user = user_,
                    grade = MemberShip.Grades.CLM )
            else:
                cell_members.filter(user = user_).update(grade = MemberShip.Grades.CLM)
        else:
            mbr = cell_members.filter(grade = MemberShip.Grades.CLM)
            if mbr[0].user != user_:
                mbr.update(
                    grade = MemberShip.Grades.MBR
                )
                cell_members.filter(user = user_).update(
                    grade = MemberShip.Grades.CLM
                )