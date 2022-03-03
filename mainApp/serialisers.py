from .models import *
from rest_framework import serializers

class PostSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
