# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Contacts(models.Model):
    #name of the person
    name = models.CharField(max_length=255, null=False)
    #email of the person
    email = models.EmailField(max_length=70, null=False, unique=True)
