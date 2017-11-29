# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import CreateView
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myImageImmersion.models import Document
from myImageImmersion.forms import DocumentForm

# def index(request):
#    today = datetime.now().date()
#    return render(request, "index.html", {"today" : today})
#-*- coding: utf-8 -*-
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
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
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse(display))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request,'edit.html',
        {'documents': documents, 'form': form})

def display(request):
    return render(request,'display.html',{})

def index(request):
    return render(request,'index.html',{})
