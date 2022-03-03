from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.enums import IntegerChoices, TextChoices
from django.db.models.fields import (
    AutoField,
    BooleanField, 
    CharField, 
    DateTimeField,
    SmallIntegerField, 
    TextField,
    URLField
)
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# Create your models here.

User = get_user_model()

class Club(models.Model):
    id_club = models.AutoField(primary_key=True)
    name = CharField(max_length=50)
    description = TextField()
    logo = models.ImageField()

    def __str__(self):
        return self.name

class Cell(models.Model):
    id_cell = AutoField(primary_key=True)
    club = ForeignKey(Club, models.CASCADE)
    name = CharField(max_length=50)
    desc = TextField(max_length=500, null=True)

    def __str__(self):
        return self.name

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

    user = ForeignKey(User, models.CASCADE)
    club = ForeignKey(Club, models.CASCADE)
    grade = CharField(max_length=3, choices=Grades.choices, default = Grades.MBR)
    cell = ForeignKey(Cell, models.SET_NULL, null=True, blank=True)
    date_of_join = DateTimeField(auto_now=True)
    state = SmallIntegerField(choices=State.choices, default=0)
    presentation = TextField(max_length=1000, null=True) #added in dec 31th,2021 17:06
    notif_setting = CharField(
        max_length= 4,
        choices= Notification.choices,
        default= Notification.BOTH
    )

    def __str__(self):
        return str(self.user) + " -- " + str(self.club)

class Post(models.Model):

    class Categories(TextChoices):
        INF = 'INF', ('INFORMATIVE')
        TRN = 'TRN', ('TRAINING_SESSION')
        STF = 'STF', ('STUFFING_SESSION')
        FRM = 'FRM', ('FORM')  

    id_post = AutoField(primary_key=True)
    title = CharField(max_length=100, null = True)
    author = ForeignKey(User, models.CASCADE)
    content = TextField()
    # pic_url = CharField(max_length=100, null=True)
    created_at = DateTimeField(auto_now=True)
    modified_at = DateTimeField(auto_now=True)
    category = CharField(
        max_length=3,
        choices=Categories.choices,
        default = Categories.INF
    )
    club = ForeignKey(Club, models.SET_NULL, null=True)
    approved = BooleanField(default=False)

    def __str__(self):
        return self.title

class TrainingSession(models.Model):
    id_session = AutoField(primary_key=True)
    post = ForeignKey(Post, models.SET_NULL, null = True)
    limited_places = SmallIntegerField(default=0)
    started_at = DateTimeField()
    presented_by = ForeignKey(User, models.SET_NULL, null = True)
    cencelled = BooleanField(default=False)

    def __str__(self):
        return self.post.title

class TrainingRegistration(models.Model):
    user = ForeignKey(User, models.CASCADE)
    session = ForeignKey(TrainingSession, models.CASCADE)
    registered_at = DateTimeField(auto_now=True)

class JoiningSession(models.Model):
    id_session = AutoField(primary_key=True)
    post = ForeignKey(Post, models.SET_NULL, null = True)
    started_at = DateTimeField()
    end_at = DateTimeField()
    canceled = BooleanField(default=False)

# v 2
class Forms(models.Model):
    post = ForeignKey(Post, models.SET_NULL, null = True)
    content = URLField()