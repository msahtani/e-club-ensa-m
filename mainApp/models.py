from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import TextChoices
from django.db.models.fields import AutoField, BooleanField, CharField, DateTimeField, IntegerField, SmallIntegerField, TextField
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Club(models.Model):
    id_club = models.AutoField(primary_key=True)
    nom = CharField(max_length=50)
    logo = models.ImageField()
    
class Cell(models.Model):
    id_cell = AutoField(primary_key=True)
    club = ForeignKey(Club, on_delete=models.CASCADE)
    name = CharField(max_length=50)

class MemberShip(models.Model):

    grades = [
        ('PRS', 'PRESEDENT'),
        ('VPR', 'VICE_PRESEDENT'),
        ('SEC', 'SECRETARY'),
        ('TRS', 'TREASURY'),
        ('CLM', 'CELL_MANAGER'),
        ('MBR', 'MEMBER')
    ]
        

    user = ForeignKey(User, on_delete=models.CASCADE)
    club = ForeignKey(Club, on_delete=models.CASCADE)
    grade = CharField(
        max_length=3,
        choices=grades,
        default = "MBR"
    )
    cell = ForeignKey(Cell)
    date = models.DateTimeField(auto_created=True)

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

    