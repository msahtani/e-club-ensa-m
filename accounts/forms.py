from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth import authenticate as auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):

    attrs_ = {
        'class': 'form-control',
        'hint': 'password'
    }

    username = forms.CharField(
        widget=forms.TextInput(attrs=attrs_)
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_)
    )

    def clean(self, *args, **kwargs):
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