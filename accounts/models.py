from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import TextChoices
from django.db.models.fields import ( 
    CharField, 
    TextField,
    DateTimeField
)
from django.db.models.fields.related import ForeignKey

import uuid
from .utils import *

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

    def save(self, *args, **kwagrs):
        self.username = '_'.join([
            self.firstname.replace(' ', '_'),
            self.lastname.replace(' ', '_')
        ]).lower()
 
        super().save(*args, **kwagrs)


class ResetPasswordTokens(models.Model):

    TIMEOUT = timedelta(minutes=30)

    user = ForeignKey(Student, models.CASCADE, to_field='username')
    token = CharField(max_length=64)
    expire_time = DateTimeField(
        default= timezone.now() + TIMEOUT
    )

    def __str__(self):
        return self.user.username

    def get_user(self) -> Student:
        return self.user

    def expired(self) -> bool:
        expired: bool = self.expire_time < timezone.now()
        if expired:
            self.delete()
        return expired

    def save(self, *args, **kwargs):
        self.token = uuid.uuid5(uuid.NAMESPACE_URL, str(self)).hex
        super().save(*args, **kwargs)
        send_reset_password_token(self.token, self.user.email)
