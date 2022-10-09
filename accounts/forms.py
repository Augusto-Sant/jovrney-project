from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class User_form(ModelForm):
    """User Register form that takes password,username and email"""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username","email","password"]