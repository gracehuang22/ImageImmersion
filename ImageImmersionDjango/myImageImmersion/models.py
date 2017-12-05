# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
    image = models.ImageField(upload_to='documents/%Y/%m/%d')

class Files(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='documents/%Y/%m/%d')
    def __unicode__(self):
        return self.name
