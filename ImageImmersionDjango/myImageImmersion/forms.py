#-*- coding: utf-8 -*-
from django import forms

class LoginForm(forms.Form):
   user = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())


class ProfileForm(forms.Form):
   name = forms.CharField(max_length = 100)
   picture = forms.FileField()
