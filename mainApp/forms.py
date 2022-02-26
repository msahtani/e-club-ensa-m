from cProfile import label
from pyexpat import model
from attr import field
from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth import authenticate as auth
from django.contrib.auth.models import User

from .models import *

class PostForm(forms.Form):

    title_attrs={ 'class': 'form-control', 'placeholder': 'title'}
    
    content_attrs = {'class': 'form-control', 'placeholder': 'content'}

    title = forms.CharField(
        widget=forms.TextInput(attrs=title_attrs), max_length= 75, label=False, required = True
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs=content_attrs), label=False, required= True
    )