# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status
from django.test import TestCase
from .models import Contacts
from django.urls import reverse
import json

class ContactViewTest(APITestCase):

    client = APIClient()
    client = APIRequestFactory()
    @staticmethod
    def create_contact(name='', email=''):
        if name and email:
            Contacts.objects.create(name=name, email=email)

    def setUp(self):
        self.create_contact('prateek gupta', 'prateek.gupta@testmail.com')
        self.create_contact('abhijeet mishra', 'abhijeet.mishra@testmail.com')
        self.create_contact('rashmi vadhavi', 'rashmi.vadhavi@testmail.com')
        self.create_contact('peeyush jhorar', 'peeyush.jhorar@testmail.com')


class GetContactViewTest(ContactViewTest):

    def test_get_all_contact(self):
        response = self.client.get(
                reverse('contacts', kwargs={}))
        expected = Contacts.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = json.loads(response.content)
        self.assertEqual(len(result), len(expected))

class PostContactViewTest(ContactViewTest):


    def test_without_name_and_email(self):
        response = self.client.post(
                reverse('contacts')
                )
        self.assertEqual(response.status_code, 400)


    def test_without_email(self):
        response = self.client.post(
                reverse('contacts'), 
                json.dumps({'name': 'ganesh'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)


    def test_without_name(self):
        response = self.client.post(
                reverse('contacts'), 
                json.dumps({'email': 'ganesh@testmail.com'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)


    def test_invalid_email(self):
        response = self.client.post(
                reverse('contacts'), 
                json.dumps({'email': 'ganesh', 'name': 'ganesh'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)


    def test_already_present(self):
        response = self.client.post(
                reverse('contacts'),
                json.dumps({'email': 'prateek.gupta@testmail.com', 'name': 'prateek'}),
                content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_new_data(self):
        response = self.client.post(
                reverse('contacts'), 
                json.dumps({'email': 'pratik.gupta@testmail.com', 'name': 'pratik'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 201)


class PutContactViewTest(ContactViewTest):


    def test_without_email(self):
        response = self.client.put(
                reverse('contacts')
                )
        self.assertEqual(response.status_code, 400)

    def test_with_invalid_email(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek@testmail.com', 'new_name': 'prateek'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)


    def test_with_new_name(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek.gupta@testmail.com', 'new_name': 'prateek'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 201)


    def test_with_new_email(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek.gupta@testmail.com', 'new_email': 'prateekg@testmail.com'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 201)


    def test_with_new_nameand_new_email(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek.gupta@testmail.com', 'new_name': 'prateek', 'new_email': 'pg@testmail.com'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 201)


class DeleteContactViewTest(ContactViewTest):


    def test_without_email(self):
        response = self.client.put(
                reverse('contacts')
                )
        self.assertEqual(response.status_code, 400)


    def test_with_invalid_email(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek@testmail.com'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 400)

    def test_with_valid_email(self):
        response = self.client.put(
                reverse('contacts'), 
                json.dumps({'email': 'prateek.gupta@testmail.com'}),
                content_type='application/json'
                )
        self.assertEqual(response.status_code, 201)


