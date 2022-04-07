from urllib import request
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, JsonResponse, QueryDict
from django.views import View
from .models import *
from datetime import datetime as dt
from django.utils.timezone import make_aware, now
from utils import fields
from django.db.models import Q

def club(cname: str):
    cname = cname.replace('-', ' ')
    return get_object_or_404(Club, name=cname)

def has_perm(user_, club_, perm_):
    
    return MemberShip.objects.filter(
        club = club_,
        user = user_,
    ).filter(
        Q(permission = 1) | Q(permission=perm_)
    ).count()
        

class MembershipAPI(View):

    def __init__(self, request: HttpRequest):

        QDICT = QueryDict(request.body)
        if not has_perm(
            request.user,
            club(QDICT.get('club_name')),
            MemberShip.Permission.MNG_MBR
        ):
            return JsonResponse({
                'message': 'permossion denied ...'
            })

    def get(self, request: HttpRequest):

        # get the club object or 404
        club_ = club(request.GET.get('club_name'))

        # get membership model fields
        m_fields = fields(MemberShip)

        # get all the members record
        members = MemberShip.objects \
            .filter(club = club_) \
            .values_list(*m_fields) 
        
        # fetch all the members
        all_members = {
            key: [member for member in members if member['cell'] == key]
            for key in Cell.objects.filter(club = club_).values_list('name')
        }.update({
            "board_members" : [member for member in members if member['cell'] == None]
        })

        # return the result
        return JsonResponse(all_members)

    def post(self, request: HttpRequest):
        # get the user by the username
        user = get_object_or_404(User,
            username = request.POST.get('username')
        )

        #get the club name
        club_name = request.POST.get('club_name')

        # get the cell by the POST verb if is given by the user
        try:
            cell_ = Cell.objects.get(
                club = club(club_name),
                name = request.POST.get('cell_name')
            )
        except:
            cell_ = None

        # create a new member
        MemberShip.objects.create(
            user = user,
            club = club(club_name),
            cell = cell_,
            grade = request.POST.get('grade'),
            state = MemberShip.State.ACTIVE
        )

        # TODO : grant a permission based on grade
        return JsonResponse({
            "message": "created successfully"
        })

    def put(self, request: HttpRequest):
        pass


class JoiningSessionAPI(View):
    
    def __init__(self):

        QDICT = QueryDict(request.body)
        if not has_perm(
            request.user,
            club(QDICT.get('club_name')),
            MemberShip.Permission.MNG_MBR
        ):
            return JsonResponse({
                'message': 'permossion denied ...'
            })

    
    def post(self, request: HttpRequest, club_name):

        # TODO: check the permission ....

        # create a new joining session 
        JoiningSession.objects.create(
            club = club(club_name),
            author = request.user,
            title = request.POST['title'],
            content = request.POST['content'],
            category = Post.Categories.JNS,
            main_pic = request.FILES.get('pic'),
            end_at = make_aware(
                dt.strptime(request.POST['end_at'], '%Y-%m-%dT%H:%M')
            )
        )
    
    def post(self, request: HttpRequest, jns_id):
        
        jns = JoiningSession.objects.get(pk = jns_id)

        if jns.end_at < now():
            return JsonResponse({
                "message": "the joining session is expired ... "
            })

        if MemberShip.objects.filter(
            club = jns.club,
            user = request.user
        ).count() == 1:
            return JsonResponse({
                "message": "you're already a member in this club"
            })
        
        MemberShip.objects.create(
            club = jns.club,
            user = request.user,
        )

        return JsonResponse({
            "message": "registred successfully .... "
        })

    def put(self, request: HttpRequest, jns_id):
        
        PUT = QueryDict(request.body)
        
        JoiningSession.objects \
            .filter(pk = jns_id) \
            .update(**PUT)

        return JsonResponse({
            "message": "updated successfully ..."
        })

    def delete(self, request: HttpRequest):
        pass