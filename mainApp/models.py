from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import IntegerChoices, TextChoices
from django.db.models.fields import AutoField, BooleanField, CharField, DateTimeField,SmallIntegerField, TextField
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Club(models.Model):
    id_club = models.AutoField(primary_key=True)
    nom = CharField(max_length=50)
    description = TextField()
    logo = models.ImageField()
    
class Cell(models.Model):
    id_cell = AutoField(primary_key=True)
    club = ForeignKey(Club, on_delete=models.CASCADE)
    name = CharField(max_length=50)

class MemberShip(models.Model):

    class Grades(TextChoices):
        PRS = 'PRS', ('PRESENDENT')
        VPR = 'VPR', ('VICE_PRESEDENT')
        SEC = 'SEC', ('SECRETARY')
        TRS = 'TRS', ('TREASURY')
        CLM = 'CLM', ('CELL_MANAGER')
        MBR = 'MBR', ('MEMBER')
    
    class State(IntegerChoices):
        ACTIVE = 1
        PENDING = 0
        DISABLED = -1

    user = ForeignKey(User, on_delete=models.CASCADE)
    club = ForeignKey(Club, on_delete=models.CASCADE)
    grade = CharField(max_length=3, choices=Grades.choices, default = Grades.MBR)
    cell = ForeignKey(Cell)
    date_of_join = DateTimeField(auto_created=True)
    stuffing_session = ForeignKey('StuffingSession')
    state = SmallIntegerField(choices=State.choices, default=0)

class Post(models.Model):

    class Categories(TextChoices):
        INF = 'INF', ('INFORMATIVE')
        TRN = 'TRN', ('TRAINING_SESSION')
        STF = 'STF', ('STUFFING_SESSION')

    id_post = AutoField(primary_key=True)
    title = CharField(max_length=100)
    author = models.ForeignKey(User)
    content = TextField()
    pic_url = CharField(max_length=100)
    created_at = DateTimeField(auto_created=True)
    category = CharField(
        max_length=3,
        choices=Categories.choices,
        default = Categories.INF
    )

class TrainingSession(models.Model):
    id_session = AutoField(primary_key=True)
    post = ForeignKey(Post)
    limited_places = SmallIntegerField(default=0)
    started_at = DateTimeField()
    presented_by = ForeignKey(User)
    cencelled = BooleanField(default=False)

class TrainingRegistration(models.Model):
    user = ForeignKey(User)
    session = ForeignKey(TrainingSession)
    registered_at = DateTimeField(auto_now=True)

class StuffingSession(models.Model):
    id_session = AutoField(primary_key=True)
    post = ForeignKey(Post)
    started_at = DateTimeField()
    end_at = DateTimeField()
    canceled = BooleanField(default=False)