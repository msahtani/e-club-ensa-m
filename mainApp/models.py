from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.enums import TextChoices
from django.db.models.fields import (
    AutoField,
    BooleanField, 
    CharField, 
    DateTimeField,
    TextField,
)
from django.db.models.fields.related import ForeignKey
from club.models import Club

User = get_user_model()


class Post(models.Model):

    class Categories(TextChoices):
        INF = 'INF', ('INFORMATIVE')
        TRN = 'TRN', ('TRAINING_SESSION')
        JNS = 'JNS', ('JOINING_SESSION')
        FRM = 'FRM', ('FORM') 

    id_post = AutoField(primary_key=True)
    title = CharField(max_length=100, null = True)
    author = ForeignKey(User, models.CASCADE)
    content = TextField()
    created_at = DateTimeField(auto_now=True)
    main_pic = models.ImageField(upload_to='images/post_pics/', blank=True)
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


# class Permission(models.Model):
    
#     class Perms(IntegerChoices):

#         ALL_PRM = 1, ("all the permissions")
#         ADD_TRS = 2, ("add training session")
#         ADD_PRJ = 3, ("add projects")
#         ADD_JNS = 4, ("add joining sessions")
#         VRF_TRG = 5, ("verify a training registration")

#     code = IntegerField(choice=Perms.choices)
#     user = ForeignKey(User, models.CASCADE)
#     club = ForeignKey(Club, models.CASCADE)

    
    