# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.test import TestCase
from .models import Contacts
from django.urls import reverse
# Create your tests here.

class ContactViewTest(APITestCase):

    client = APIClient()

    @staticmethod
    def create_contact(name='', email=''):
        if name and email:
            Contacts.objects.create(name=name, email=email)


    def setUp(self):
        self.create_contact('prateek gupta', 'preteek.gupta@testmail.com')
        self.create_contact('abhijeet mishra', 'abhijeet.mishra@testmail.com')
        self.create_contact('rashmi vadhavi', 'rashmi.vadhavi@testmail.com')
        self.create_contact('peeyush jhorar', 'peeyush.jhorar@testmail.com')


class GetContactViewTest(ContactViewTest):

    def test_get_all_songs(self):
        response = self.client.get(
                reverse('contacts-all', kwargs={}))

        expected = Contacts.objects.all()
        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
