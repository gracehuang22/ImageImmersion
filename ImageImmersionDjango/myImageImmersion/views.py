# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render

from myImageImmersion.forms import ProfileForm
from myImageImmersion.models import Profile


def index(request):
   today = datetime.now().date()
   return render(request, "index.html", {"today" : today})
#-*- coding: utf-8 -*-

def SaveProfile(request):
   saved = False

   if request.method == "POST":
      #Get the posted form
      MyProfileForm = ProfileForm(request.POST, request.FILES)

      if MyProfileForm.is_valid():
         profile = Profile()
         profile.name = MyProfileForm.cleaned_data["name"]
         profile.picture = MyProfileForm.cleaned_data["picture"]
         profile.save()
         saved = True
   else:
      MyProfileForm = ProfileForm()

   return render(request, 'profile.html', locals())
