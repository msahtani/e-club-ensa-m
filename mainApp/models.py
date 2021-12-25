from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
# Create your models here.

class Club(models.Model):
    id_club = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    logo = models.ImageField()
    

class MemberShip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    grade = models.CharField(
    )
    date = models.DateField(default=timezone.now())
    
