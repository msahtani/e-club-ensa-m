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
        INF = 'INF', ('ARTICLE')
        TRN = 'TRN', ('TRAINING_SESSION')
        JNS = 'JNS', ('JOINING_SESSION')
        FRM = 'FRM', ('FORM') 

    id_post = AutoField(primary_key=True)
    title = CharField(max_length=100, null = True)
    author = ForeignKey(User, models.CASCADE)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    main_pic = models.ImageField(upload_to='images/post_pics/', blank=True)
    
    category = CharField(
        max_length=3,
        choices=Categories.choices
    )
    club = ForeignKey(Club, models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Article(Post):
    approved = BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.category = Post.Categories.INF
        super().save(*args, **kwargs)