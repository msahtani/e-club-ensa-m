from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.enums import IntegerChoices, TextChoices
from django.db.models.fields import (
    BooleanField, 
    CharField, 
    DateTimeField,
    SmallIntegerField, 
    TextField,
)
from django.db.models.fields.related import ForeignKey
# TODO: import Club, Cell, Post
from club.models import *
from mainApp.models import *

User = get_user_model()

# Create your models here.
class MemberShip(models.Model):
    
    class Grades(TextChoices):
        PRS = 'PRS', ('PRESENDENT')
        VPR = 'VPR', ('VICE_PRESEDENT')
        SEC = 'SEC', ('SECRETARY')
        TRS = 'TRS', ('TREASURY')
        CLM = 'CLM', ('CELL_MANAGER')
        MBR = 'MBR', ('MEMBER')
    
    class State(IntegerChoices):
        ACTIVE = 1    # 
        PENDING = 0   # 
        DISABLED = -1 # 

    class Notification(TextChoices):
        NONE = "NONE", ('no notifications')
        INAP = "INAP", ('in-app only')
        MAIL = "MAIL", ('email only')
        BOTH = "BOTH", ('in-app and email')

    class Permission(IntegerChoices):
        ALL_PRM = 1, ("all the permissions")
        MNG_TRS = 2, ("manage training session")
        MNG_PRJ = 3, ("manage projects")
        MNG_MBR = 4, ("mamange joining sessions")
        VRF_TRG = 5, ("verify a training registration")

    user = ForeignKey(User, models.CASCADE)
    club = ForeignKey(Club, models.CASCADE)
    grade = CharField(max_length=3, choices=Grades.choices, default = Grades.MBR)
    cell = ForeignKey(Cell, models.SET_NULL, null=True, blank=True)
    date_of_join = DateTimeField(auto_now=True)
    state = SmallIntegerField(choices=State.choices, default=0)
    presentation = TextField(max_length=1000, blank=True) #added in dec 31th,2021 17:06
    notif_setting = CharField(max_length= 4,choices= Notification.choices, default= Notification.BOTH)
    permission = SmallIntegerField(choices=Permission.choices, null=True)

    def __str__(self):
        return str(self.user) + " -- " + str(self.club)

class JoiningSession(Post):
    started_at = DateTimeField()
    end_at = DateTimeField()
    canceled = BooleanField(default=False)