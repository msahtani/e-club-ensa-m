from cProfile import label
from pyexpat import model
from attr import field
from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth import authenticate as auth
from django.contrib.auth.models import User

from .models import *

class addPostForm(forms.Form):

    title_attrs={
        'class': 'form-control',
        'placeholder': 'title'
    }
    content_attrs = {
        'class': 'form-control',
        'placeholder': 'content'
    }

    title = forms.CharField(
        widget=forms.TextInput(attrs=title_attrs), max_length= 75, label=False, required = True
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs=content_attrs), label=False, required= True
    )

    
    # title = forms.TextInput(
    #     attrs = {'placeholder': 'title'},
    #     label = False, required = True
    # )
    # content = forms.Textarea(required = True)

""""
class LoginForm(forms.Form):

    __user_attrs_ = {
        
        'placeholder': 'username'
    }
    __pass_attrs = {
        
        'placeholder': 'password'
    }

    username = forms.CharField(
        widget=forms.TextInput(attrs=__user_attrs_), label=False, required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=__pass_attrs), label=False
    )

    def clean(self, *args, **kwargs):
        print(self.cleaned_data)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except:
                raise forms.ValidationError("This user does not exists")
            
            user = auth(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user id not active")
        
        return super(LoginForm, self).clean(*args, **kwargs)

"""