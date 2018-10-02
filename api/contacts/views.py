# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from .models import Contacts


class BadRequest(Exception):
    """
    This is just to check the incoming request.
    """
    pass

def validate_request(data, required_params):
    if not set(required_params).issubset(set(data.keys())):
        raise BadRequest('Invalid request. %s is/are compulsory' %", ".join(required_params))


@csrf_exempt
def contacts(request):
    if request.method == 'GET':
        """
        Handle get request. This is pagination based.
        By default we have assumed per page ocntent to be 10
        """
        status_code = 200
        contact_list = Contacts.objects.all()
        #get the page number
        page = request.GET.get('page', 1)
        paginator = Paginator(contact_list, 10)

        #get the page data
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        contact_list = []

        #create the list
        for contact in contacts:
            contact_list.append({'name': contact.name,
                                'email': contact.email})
        message = json.dumps({'contacts': contact_list})

    elif request.method == 'POST':
        """
        Handle post request. This is to create a new contact.
        Email and name is compulsory to create any record.
        """

        status_code = 201
        required_params = ['email', 'name']
        data = json.loads(request.body)

        try:
            validate_request(data, required_params)
            if Contacts.objects.filter(email=data['email']):
                raise BadRequest('%s email is already registered.Please try a different one.' %data['email'])
            contact = Contacts.objects.create(name=data['name'], email=data['email'])
            message = 'New contact created for %s' %data['name']
        except BadRequest as error:
            status_code = 400
            message = error.message
        except Exception as error:
            status_code = 500
            message = error.message

    elif request.method == 'PUT':
        """
        Handle put request. This is for editing the name.
        Email is compulsory to create any record.
        to update, you have to pass new_email and new_name.
        """

        status_code = 201
        required_params = ['email']
        data = json.loads(request.body)

        try:
            validate_request(data, required_params)
            contact = Contacts.objects.get(email=data['email'])
            if 'new_email' in data:
                check = Contacts.objects.filter(email=data['new_email'])
                if check:
                    raise BadRequest('%s email is already a regsitered. Please select a new one' %data['new_email'])
                else:
                    contact.email = data['new_email']
            if 'new_name' in data:
                contact.name = data['new_name']
            contact.save()
            message = "Contact updated for %s email" %data['email']
        except ObjectDoesNotExist as error:
            status_code = 400
            message = "%s email does not exists" %data['email']
        except BadRequest as error:
            status_code = 400
            message = error.message
        except Exception as error:
            status_code = 500
            message = error.message

    elif request.method == 'DELETE':
        """
        Handle delete request.
        Email address in compulsory for this.
        """

        status_code = 200
        data = json.loads(request.body)
        try:
            validate_request(data, ['email'])
            contact = Contacts.objects.get(email=data['email'])
            contact.delete()
            message = "Contact deleted for %s" %contact.name
        except BadRequest as error:
            status_code = 400
            message = error.message
        except ObjectDoesNotExist:
            status_code = 400
            message = "%s email does not exists." %data['email']
        except Exception as error:
            status_code = 500
            message = error.message
    return HttpResponse(content=message, status=status_code)


@csrf_exempt
def search(request):
    if request.method == 'GET':
        """
        Handle get request. This is pagination based.
        By default we have assumed per page ocntent to be 10
        """
        status_code = 200
        contact_list = Contacts.objects.all()
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        page = request.GET.get('page', 1)

        #filter out the required data
        if name:
            contact_list.filter(name=name)
        if email:
            contact_list.filter(email=email)

        paginator = Paginator(contact_list, 10)

        #get the page data
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        contact_list = []

        #create the list
        for contact in contacts:
            contact_list.append({'name': contact.name,
                                'email': contact.email})
        message = json.dumps({'contacts': contact_list})
    else:
        status_code = 405
        message = 'Method not allowed'
    return HttpResponse(status=status_code, content=message)
