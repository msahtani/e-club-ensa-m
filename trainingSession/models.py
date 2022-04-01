from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import (
    AutoField,
    CharField,  
    TextField,
    SmallIntegerField,
    DateTimeField,
    BooleanField
)
from django.db.models.fields.related import ForeignKey

from mainApp.models import Post

User = get_user_model()
# Create your models here.
class TrainingSession(Post):
    limited_places = SmallIntegerField(default=0)
    started_at = DateTimeField()
    presented_by = ForeignKey(User, models.SET_NULL, null = True)
    cencelled = BooleanField(default=False)

    def __str__(self):
        return self.id_post


class TrainingRegistration(models.Model):
    user = ForeignKey(User, models.CASCADE)
    session = ForeignKey(TrainingSession, models.CASCADE)
    token = CharField(max_length=64, blank=True)
    confirmed = BooleanField(default=False)
    registered_at = DateTimeField(auto_now=True)