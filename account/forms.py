from django.contrib.auth.models import User
from django import forms

class RegisterUser(forms.ModelForm):
    password = forms.CharField(max_length=250,widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=250,widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','password_confirm',)

class LoginUser(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(max_length=250,widget=forms.PasswordInput())