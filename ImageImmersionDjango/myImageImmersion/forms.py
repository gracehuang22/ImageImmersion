#-*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    image = forms.ImageField(
        label='Select a file',
    )

class ImageForm(forms.Form):
    fname = forms.CharField(label='File name', max_length=100)
