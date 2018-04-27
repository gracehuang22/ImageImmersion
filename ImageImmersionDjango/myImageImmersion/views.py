# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.shortcuts import redirect
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

from seamCarving import main

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
        orig = request.POST.get('orig_image', False)
        binary_data = a2b_base64(data[1])
        fd = open(filename, 'w+')
        fd.write(binary_data)
        file_data = Files(name=filename)
        file_data.image.save(filename, File(fd))
        fd.close()

        documents = Document.objects.all()
        #get recent picture
        cwd = os.getcwd()
        print(cwd)
        recentPic = cwd + '/myImageImmersion' + documents.last().image.url
        files = Files.objects.all()
        recentMask = cwd+ '/myImageImmersion' + files.last().image.url
        print("\n recentpic: " + recentPic + " , " + recentMask)
        #run seamCarving on picture and mask
        output = main(recentPic,recentMask)
        print("doneSeam")


        return HttpResponseRedirect(reverse(final))

def display(request):
    # if post, get file path of mask and og picture
    #show result of seamCarving
    print("gotrequest: ", request)
    if request.method == 'GET':
        documents = Document.objects.all()
        #get recent picture
        cwd = os.getcwd()
        print(cwd)
        recentPic = cwd + '/myImageImmersion' + documents.last().image.url
        files = Files.objects.all()
        recentMask = cwd+ '/myImageImmersion' + files.last().image.url
        print("\n recentpic: " + recentPic + " , " + recentMask)
        #run seamCarving on picture and mask
        output = main(recentPic,recentMask)
        print("doneSeam")

        newdoc = Document(image = cwd + "/" + output)
        # print ("output: " + output)
        newdoc.save()

        # Render list page with the documents and the form
        return HttpResponseRedirect(reverse(final))


def final(request):
    documents = Document.objects.all()
    return render(request,'display.html',{'documents': documents})

def index(request):
    return render(request,'index.html',{})
