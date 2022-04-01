from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import IntegerChoices, TextChoices
from django.db.models.fields import ( 
    CharField, 
    TextField,
)
from django.forms import ImageField

# Create your models here.
class Student(AbstractUser):
    
    class Level(TextChoices):
        CP1 = 'CP1'
        CP2 = 'CP2'
        SEECS1, SEECS2, SEECS3 = 'SEECS1', 'SEECS2', 'SEECS3'
        G11, G12, G13 = 'G11', 'G12', 'G13'
        GIL1, GIL2, GIL3 = 'GIL1', 'GIL2', 'GIL3'
        GCDSTE1, GCDSTE2, GCDSTE3 = 'GCDSTE1', 'GCDSTE2', 'GCDSTE3'
        RSSP1, RSSP2, RSSP3 = 'RSSP1', 'RSSP2', 'RSSP3'
        
    level = CharField(
        max_length=7,
        choices= Level.choices,
        default= Level.CP1
    )
    phone_number = CharField(max_length=13, blank=True)
    avatar = models.ImageField(upload_to='image/avatars', blank=True)
    bio = TextField(blank=True)