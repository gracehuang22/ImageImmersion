# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import CreateView
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
#from urllib import parse as urlparse
from binascii import a2b_base64

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myImageImmersion.models import Document
from myImageImmersion.models import Files
from myImageImmersion.forms import DocumentForm
from myImageImmersion.forms import ImageForm

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(image = request.FILES['image'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse(edit))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request,'upload.html',
        {'documents': documents, 'form': form})

def edit(request):
    print("gotrequest: ", request)
    if request.method == 'GET':
        documents = Document.objects.all()
        form = ImageForm()
        # Render list page with the documents and the form
        return render(request,'edit.html',
                {'documents': documents, 'form': form})
    elif request.method == 'POST':
        filename = request.POST.get('save_fname', False)
        data = request.POST.get('save_cdata', False)
        data = data.split(",")
        binary_data = a2b_base64(data[1])
        fd = open(filename, 'w+')
        fd.write(binary_data)
        file_data = Files(name=filename)
        file_data.image.save(filename, File(fd))
        fd.close()
        return HttpResponseRedirect(reverse(display))


def display(request):
    return render(request,'display.html',{})

def index(request):
    return render(request,'index.html',{})
