from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.enums import IntegerChoices, TextChoices
from django.db.models.fields import (
    AutoField,
    CharField,  
    TextField,
)
from django.db.models.fields.related import ForeignKey

from django.db import models

# Create your models here.

class Club(models.Model):
    id_club = models.AutoField(primary_key=True)
    name = CharField(max_length=50)
    description = TextField()
    logo = models.ImageField(upload_to="images/club_logos")

    def __str__(self):
        return self.name

class Cell(models.Model):
    id_cell = AutoField(primary_key=True)
    club = ForeignKey(Club, models.CASCADE)
    name = CharField(max_length=50)
    desc = TextField(max_length=500, null=True)

    def __str__(self):
        return self.name