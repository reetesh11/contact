# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class Contacts(models.Model):
    #name of the person
    name = models.CharField(max_length=255, null=False)
    #email of the person
    email = models.EmailField(max_length=70, null=False, unique=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        if self.email != "":
            validate_email(self.email)
        super(Contact, self).save(*args, **kwargs)
